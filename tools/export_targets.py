#!/usr/bin/env python3
"""
OpenSTEM University Partner Sync & Exporter
Fetches, parses, and normalizes university records from all 15 country sheets
in Google Sheets ID: 1qIFVwUn3xr0eVkOohm0hArRtUaENBfqoeyqetr75Iak
"""

import subprocess
import json
import csv
import re
import os
import sys

SPREADSHEET_ID = "1qIFVwUn3xr0eVkOohm0hArRtUaENBfqoeyqetr75Iak"

SHEETS = [
    ("CANADA OUTPUT", "Canada"),
    ("USA OUTPUT", "USA"),
    ("UK OUTPUT", "UK"),
    ("AUSTRALIA OUTPUT", "Australia"),
    ("GERMANY OUTPUT", "Germany"),
    ("ITALY OUTPUT", "Italy"),
    ("SWITZERLAND OUTPUT", "Switzerland"),
    ("NETHERLANDS OUTPUT", "Netherlands"),
    ("SWEDEN OUTPUT", "Sweden"),
    ("JAPAN OUTPUT", "Japan"),
    ("FRANCE OUTPUT", "France"),
    ("SPAIN OUTPUT", "Spain"),
    ("DENMARK OUTPUT", "Denmark"),
    ("HUNGARY OUTPUT", "Hungary"),
    ("NEW ZEALAND OUTPUT", "New Zealand"),
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_sheet_rows(sheet_name):
    print(f"Fetching {sheet_name}...")
    cmd = ["gsheets", "readonly", "read", SPREADSHEET_ID, f"'{sheet_name}'!A1:AZ450"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading {sheet_name}: {res.stderr}", file=sys.stderr)
        return []
    
    raw_lines = res.stdout.strip().split("\n")
    if not raw_lines:
        return []
    
    rows = []
    for line in raw_lines:
        if line.strip():
            rows.append([cell.strip() for cell in line.split("\t")])
    return rows

def find_col_index(headers, patterns):
    for i, h in enumerate(headers):
        h_lower = h.lower()
        for p in patterns:
            if re.search(p, h_lower):
                return i
    return -1

def normalize_email(val):
    if not val:
        return ""
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', val)
    return emails[0] if emails else ""

def parse_sheet(sheet_name, default_country):
    rows = fetch_sheet_rows(sheet_name)
    if not rows:
        return []
    
    headers = rows[0]
    
    # Identify indices
    name_idx = find_col_index(headers, [r'university / institution', r'institution', r'university', r'school', r'provider', r'counterparty', r'hei'])
    if name_idx == -1:
        name_idx = 0 if len(headers) > 0 else -1
        
    country_idx = find_col_index(headers, [r'^country$'])
    state_idx = find_col_index(headers, [r'state', r'province', r'region', r'city', r'nation', r'campus'])
    website_idx = find_col_index(headers, [r'university website', r'home page', r'official institution website', r'website'])
    partner_page_idx = find_col_index(headers, [r'partner.*page', r'partnership.*page', r'partner.*link', r'agent.*link', r'agent.*application', r'agent.*form', r'agent.*resources', r'policy.*link', r'evidence.*application'])
    email_idx = find_col_index(headers, [r'email'])
    phone_idx = find_col_index(headers, [r'phone', r'tel'])
    evidence_idx = find_col_index(headers, [r'evidence class', r'evidence grade', r'commission proof level'])
    priority_idx = find_col_index(headers, [r'priority'])
    programs_idx = find_col_index(headers, [r'program', r'programme', r'course', r'scope'])
    action_idx = find_col_index(headers, [r'next action', r'next step', r'partnership step', r'recommended outreach step'])
    assessment_idx = find_col_index(headers, [r'openstem assessment', r'openstem judgement'])
    requirements_idx = find_col_index(headers, [r'agent requirements', r'vetting', r'requirements', r'company checks'])

    records = []
    for row_num, row in enumerate(rows[1:], start=2):
        if not row or not any(row):
            continue
        
        def get_val(idx):
            return row[idx].strip() if 0 <= idx < len(row) else ""
        
        name = get_val(name_idx)
        if not name or name.lower() in ["total", "country", "source"]:
            continue
        
        country = get_val(country_idx) or default_country
        state_or_city = get_val(state_idx)
        website = get_val(website_idx)
        partner_page = get_val(partner_page_idx)
        raw_email = get_val(email_idx)
        email = normalize_email(raw_email)
        phone = get_val(phone_idx)
        evidence = get_val(evidence_idx)
        priority = get_val(priority_idx)
        programs = get_val(programs_idx)
        action = get_val(action_idx)
        assessment = get_val(assessment_idx)
        requirements = get_val(requirements_idx)
        
        # Determine clean priority if missing
        if not priority:
            if "p1" in action.lower() or "direct named person" in assessment.lower():
                priority = "P1"
            elif email or partner_page:
                priority = "P2"
            else:
                priority = "P3"
        elif "p1" in priority.lower():
            priority = "P1"
        elif "p2" in priority.lower():
            priority = "P2"
        elif "p3" in priority.lower():
            priority = "P3"

        records.append({
            "id": f"{default_country[:3].upper()}-{len(records)+1:03d}",
            "name": name,
            "country": country,
            "state_or_city": state_or_city,
            "website": website,
            "partner_page": partner_page,
            "email": email,
            "raw_email": raw_email,
            "phone": phone,
            "evidence_grade": evidence,
            "priority": priority,
            "programs": programs,
            "assessment": assessment,
            "next_action": action,
            "requirements": requirements,
            "source_sheet": sheet_name,
            "row_number": row_num
        })
    
    print(f"  Parsed {len(records)} institutions from {sheet_name}")
    return records

def main():
    print("Starting OpenSTEM University Dataset Extraction...")
    all_records = []
    
    for sheet_name, country in SHEETS:
        records = parse_sheet(sheet_name, country)
        all_records.extend(records)
        
    print(f"\nTotal institutions extracted: {len(all_records)}")
    
    json_path = os.path.join(DATA_DIR, "targets.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to: {json_path}")
    
    csv_path = os.path.join(DATA_DIR, "targets.csv")
    fieldnames = [
        "id", "name", "country", "state_or_city", "priority", "email",
        "partner_page", "website", "evidence_grade", "programs", "next_action",
        "source_sheet", "row_number"
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_records)
    print(f"Saved CSV to: {csv_path}")

    # Generate summary statistics
    stats = {}
    for r in all_records:
        c = r["country"]
        if c not in stats:
            stats[c] = {"total": 0, "has_email": 0, "has_partner_page": 0, "P1": 0, "P2": 0, "P3": 0}
        stats[c]["total"] += 1
        if r["email"]:
            stats[c]["has_email"] += 1
        if r["partner_page"]:
            stats[c]["has_partner_page"] += 1
        p = r["priority"]
        if p in stats[c]:
            stats[c][p] += 1
            
    stats_path = os.path.join(DATA_DIR, "country_summary.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved Country Summary to: {stats_path}")
    
    print("\nExtraction & Sync Complete.")

if __name__ == "__main__":
    main()
