import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "openstem.db")
JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "openstem_field_data.json")

def init_db(force=False):
    if os.path.exists(DB_PATH) and not force:
        return
    
    print("Building OpenSTEM SQLite search database...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY,
            title TEXT,
            university TEXT,
            country TEXT,
            location TEXT,
            subject TEXT,
            type TEXT,
            funding TEXT,
            deadline TEXT,
            source TEXT,
            gpa TEXT,
            ielts TEXT,
            gre TEXT,
            desc TEXT,
            raw_json TEXT
        )
    """)

    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS opportunities_fts USING fts5(
            title, university, country, subject, type, funding, desc, content='opportunities', content_rowid='id'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS researchers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            title TEXT,
            subject TEXT,
            university TEXT,
            country TEXT,
            email TEXT,
            topics TEXT,
            summary TEXT,
            source TEXT,
            raw_json TEXT
        )
    """)

    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS researchers_fts USING fts5(
            name, title, subject, university, country, topics, summary, content='researchers', content_rowid='id'
        )
    """)

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        opps = data.get("opportunities", [])
        for o in opps:
            reqs = o.get("requirements", {})
            if isinstance(reqs, dict):
                gpa = reqs.get("gpa", "") or ""
                ielts = reqs.get("ielts", "") or ""
                gre = reqs.get("gre", "") or ""
            else:
                gpa = str(reqs or "")
                ielts = ""
                gre = ""

            cur.execute("""
                INSERT OR REPLACE INTO opportunities (
                    id, title, university, country, location, subject, type,
                    funding, deadline, source, gpa, ielts, gre, desc, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                o.get("id"),
                o.get("title", ""),
                o.get("university", ""),
                o.get("country", ""),
                o.get("location", ""),
                o.get("subject", ""),
                o.get("type", ""),
                o.get("funding", ""),
                o.get("deadline", ""),
                o.get("source", ""),
                gpa,
                ielts,
                gre,
                o.get("desc", ""),
                json.dumps(o)
            ))
            cur.execute("""
                INSERT INTO opportunities_fts(rowid, title, university, country, subject, type, funding, desc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                o.get("id"),
                o.get("title", ""),
                o.get("university", ""),
                o.get("country", ""),
                o.get("subject", ""),
                o.get("type", ""),
                o.get("funding", ""),
                o.get("desc", "")
            ))

        res = data.get("researchers", [])
        for r in res:
            topics_str = ", ".join(r.get("topics", [])) if isinstance(r.get("topics"), list) else str(r.get("topics", ""))
            cur.execute("""
                INSERT OR REPLACE INTO researchers (
                    id, name, title, subject, university, country, email,
                    topics, summary, source, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r.get("id"),
                r.get("name", ""),
                r.get("title", ""),
                r.get("subject", ""),
                r.get("university", ""),
                r.get("country", ""),
                r.get("email", ""),
                topics_str,
                r.get("summary", ""),
                r.get("source", ""),
                json.dumps(r)
            ))
            cur.execute("""
                INSERT INTO researchers_fts(rowid, name, title, subject, university, country, topics, summary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r.get("id"),
                r.get("name", ""),
                r.get("title", ""),
                r.get("subject", ""),
                r.get("university", ""),
                r.get("country", ""),
                topics_str,
                r.get("summary", "")
            ))

    conn.commit()
    conn.close()
    print("Database built successfully!")

def search_opportunities(query=None, country=None, opp_type=None, subject=None, limit=5, offset=0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    conditions = []
    params = []

    if query and query.strip():
        # Sanitize query for FTS
        clean_q = "".join([c if c.isalnum() or c.isspace() else " " for c in query]).strip()
        if clean_q:
            conditions.append("id IN (SELECT rowid FROM opportunities_fts WHERE opportunities_fts MATCH ?)")
            params.append(f"{clean_q}*")

    if country and country.lower() != "all":
        if country.upper() == "USA" or country.lower() == "united states":
            conditions.append("(country LIKE '%USA%' OR country LIKE '%United States%')")
        elif country.upper() == "UK" or country.lower() == "united kingdom":
            conditions.append("(country LIKE '%UK%' OR country LIKE '%United Kingdom%')")
        else:
            conditions.append("country LIKE ?")
            params.append(f"%{country}%")

    if opp_type and opp_type.lower() != "all":
        if "master" in opp_type.lower():
            conditions.append("type LIKE '%Master%'")
        elif "phd" in opp_type.lower() or "doctoral" in opp_type.lower():
            conditions.append("(type LIKE '%PhD%' OR type LIKE '%Doctoral%')")
        elif "scholarship" in opp_type.lower():
            conditions.append("type LIKE '%Scholarship%'")
        elif "internship" in opp_type.lower():
            conditions.append("type LIKE '%Internship%'")
        elif "fellowship" in opp_type.lower():
            conditions.append("type LIKE '%Fellowship%'")
        elif "research" in opp_type.lower():
            conditions.append("type LIKE '%Research%'")
        else:
            conditions.append("type LIKE ?")
            params.append(f"%{opp_type}%")

    if subject and subject.lower() != "all":
        conditions.append("subject LIKE ?")
        params.append(f"%{subject}%")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # Total count query
    count_sql = f"SELECT COUNT(*) FROM opportunities {where_clause}"
    cur.execute(count_sql, params)
    total_count = cur.fetchone()[0]

    # Paginated data query
    sql = f"""
        SELECT id, title, university, country, type, funding, deadline, source, gpa, ielts, gre, desc
        FROM opportunities
        {where_clause}
        ORDER BY CASE WHEN deadline IS NOT NULL AND deadline != '' THEN 0 ELSE 1 END, deadline DESC
        LIMIT ? OFFSET ?
    """
    cur.execute(sql, params + [limit, offset])
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows, total_count

def get_opportunity_by_id(opp_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM opportunities WHERE id = ?", (opp_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def search_researchers(query=None, subject=None, country=None, limit=5, offset=0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    conditions = []
    params = []

    if query and query.strip():
        clean_q = "".join([c if c.isalnum() or c.isspace() else " " for c in query]).strip()
        if clean_q:
            conditions.append("id IN (SELECT rowid FROM researchers_fts WHERE researchers_fts MATCH ?)")
            params.append(f"{clean_q}*")

    if country and country != "All":
        conditions.append("country LIKE ?")
        params.append(f"%{country}%")

    if subject and subject.lower() != "all":
        conditions.append("subject LIKE ?")
        params.append(f"%{subject}%")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    count_sql = f"SELECT COUNT(*) FROM researchers {where_clause}"
    cur.execute(count_sql, params)
    total_count = cur.fetchone()[0]

    sql = f"""
        SELECT id, name, title, subject, university, country, email, topics, summary, source
        FROM researchers
        {where_clause}
        ORDER BY id ASC
        LIMIT ? OFFSET ?
    """
    cur.execute(sql, params + [limit, offset])
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows, total_count

def get_researcher_by_id(res_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM researchers WHERE id = ?", (res_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

TARGETS_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "targets.json")

def init_waiting_universities():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS waiting_universities (
            id TEXT PRIMARY KEY,
            name TEXT,
            country TEXT,
            state_or_city TEXT,
            url TEXT,
            programs TEXT,
            assessment TEXT,
            evidence_grade TEXT,
            priority TEXT,
            raw_json TEXT
        )
    """)
    cur.execute("SELECT COUNT(*) FROM waiting_universities")
    count = cur.fetchone()[0]
    if count == 0 and os.path.exists(TARGETS_JSON_PATH):
        with open(TARGETS_JSON_PATH, "r", encoding="utf-8") as f:
            targets = json.load(f)
        for t in targets:
            url = t.get("partner_page") or t.get("website") or ""
            if not url.startswith("http"):
                url = "https://openstemrecruitment.com/"
            cur.execute("""
                INSERT OR REPLACE INTO waiting_universities (
                    id, name, country, state_or_city, url, programs, assessment, evidence_grade, priority, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t.get("id"),
                t.get("name", ""),
                t.get("country", ""),
                t.get("state_or_city", ""),
                url,
                t.get("programs", ""),
                t.get("assessment", ""),
                t.get("evidence_grade", ""),
                t.get("priority", ""),
                json.dumps(t)
            ))
        conn.commit()
    conn.close()

def get_waiting_university_countries():
    init_waiting_universities()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT country, COUNT(*) as cnt FROM waiting_universities GROUP BY country ORDER BY cnt DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_waiting_universities_by_country(country=None, limit=3, offset=0):
    init_waiting_universities()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    conditions = []
    params = []
    if country and country.lower() != "all":
        conditions.append("country = ?")
        params.append(country)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    count_sql = f"SELECT COUNT(*) FROM waiting_universities {where_clause}"
    cur.execute(count_sql, params)
    total_count = cur.fetchone()[0]

    sql = f"""
        SELECT id, name, country, state_or_city, url, programs, assessment, evidence_grade, priority
        FROM waiting_universities
        {where_clause}
        ORDER BY name ASC
        LIMIT ? OFFSET ?
    """
    cur.execute(sql, params + [limit, offset])
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows, total_count

if __name__ == "__main__":
    init_db(force=True)
    opps, count = search_opportunities(query="quantum", limit=2)
    print(f"Sample opportunity query returned {count} results. Sample 0 title: {opps[0]['title'] if opps else 'None'}")
    res, r_count = search_researchers(query="physics", limit=2)
    print(f"Sample researcher query returned {r_count} results. Sample 0 name: {res[0]['name'] if res else 'None'}")
