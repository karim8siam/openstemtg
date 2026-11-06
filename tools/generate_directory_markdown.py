#!/usr/bin/env python3
"""
Generates the comprehensive Master Markdown Directory of all extracted emails
across all 15 countries.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "all_university_emails.json")
OUTPUT_MD = "/Users/karimsiam/.gemini/antigravity/brain/4883dddd-064d-4afd-82e2-796ec0c78912/master_all_countries_email_directory.md"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

by_country = {}
for r in records:
    c = r["country"]
    if c not in by_country:
        by_country[c] = []
    by_country[c].append(r)

out = []
out.append("# 🌍 OpenSTEM Master Global University & Agent Email Directory")
out.append(f"> **Database Scope:** All 15 Countries Across 1,000+ Target Institutions  ")
out.append(f"> **Total Email Records:** {len(records)} | **Total Unique Emails:** {len(set(r['email'] for r in records))}  ")
out.append(f"> **Master CSV:** [`data/all_university_emails.csv`](file://{os.path.abspath(os.path.join(BASE_DIR, 'data', 'all_university_emails.csv'))})  ")
out.append(f"> **Raw Text List:** [`data/all_email_recipients_plain_list.txt`](file://{os.path.abspath(os.path.join(BASE_DIR, 'data', 'all_email_recipients_plain_list.txt'))})  \n")
out.append("---\n")

for country, items in by_country.items():
    out.append(f"## 📍 {country} ({len(items)} Verified Contacts)\n")
    out.append("| Institution | Verified Email Address | Role / Department | State / City | Action / Portal |")
    out.append("|---|---|---|---|---|")
    for it in items:
        inst = it["institution"].replace("|", "-")
        em = it["email"]
        role = it["email_type"].replace("|", "-")
        loc = it["state_or_city"].replace("|", "-") or "-"
        portal = it["portal_link"]
        portal_disp = f"[Link]({portal})" if portal and portal.startswith("http") else "-"
        out.append(f"| **{inst}** | `{em}` | {role} | {loc} | {portal_disp} |")
    out.append("\n---\n")

content = "\n".join(out)
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Generated {OUTPUT_MD} successfully ({len(records)} rows)")
