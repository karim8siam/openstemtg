#!/usr/bin/env python3
"""
OpenSTEM University Outreach Pipeline Manager
Interactive CLI for managing leads, generating tailored email pitches,
tracking relationship stages, and driving the 1,000+ university partnership roadmap.
"""

import os
import sys
import json
import csv
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DRAFTS_DIR = os.path.join(BASE_DIR, "drafts")
TARGETS_FILE = os.path.join(DATA_DIR, "targets.json")
SUMMARY_FILE = os.path.join(DATA_DIR, "country_summary.json")
STATUS_FILE = os.path.join(DATA_DIR, "pipeline_status.json")

os.makedirs(DRAFTS_DIR, exist_ok=True)

def load_targets():
    if not os.path.exists(TARGETS_FILE):
        print(f"Error: {TARGETS_FILE} not found. Run 'python3 tools/export_targets.py' first.", file=sys.stderr)
        sys.exit(1)
    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_status():
    if not os.path.exists(STATUS_FILE):
        return {}
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_status(status_dict):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_dict, f, indent=2, ensure_ascii=False)

def print_summary():
    targets = load_targets()
    status_dict = load_status()
    
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)
    else:
        stats = {}

    print("\n" + "="*85)
    print(" OPENSTEM GLOBAL UNIVERSITY OUTREACH PIPELINE SUMMARY")
    print("="*85)
    print(f"{'Country':<15} | {'Total':<6} | {'Emails':<7} | {'Portals':<8} | {'P1':<4} | {'P2':<4} | {'P3':<4} | {'Contacted':<9}")
    print("-" * 85)
    
    tot_univ = 0
    tot_email = 0
    tot_portals = 0
    tot_p1 = 0
    tot_p2 = 0
    tot_p3 = 0
    tot_contacted = 0
    
    for country, s in stats.items():
        c_contacted = sum(1 for t in targets if t["country"].lower() == country.lower() and t["id"] in status_dict and status_dict[t["id"]]["status"] != "IDENTIFIED")
        print(f"{country:<15} | {s['total']:<6} | {s['has_email']:<7} | {s['has_partner_page']:<8} | {s['P1']:<4} | {s['P2']:<4} | {s['P3']:<4} | {c_contacted:<9}")
        tot_univ += s['total']
        tot_email += s['has_email']
        tot_portals += s['has_partner_page']
        tot_p1 += s['P1']
        tot_p2 += s['P2']
        tot_p3 += s['P3']
        tot_contacted += c_contacted
        
    print("-" * 85)
    print(f"{'TOTAL (15)':<15} | {tot_univ:<6} | {tot_email:<7} | {tot_portals:<8} | {tot_p1:<4} | {tot_p2:<4} | {tot_p3:<4} | {tot_contacted:<9}")
    print("="*85 + "\n")

def list_targets(args):
    targets = load_targets()
    status_dict = load_status()
    
    filtered = targets
    if args.country:
        filtered = [t for t in filtered if t["country"].lower() == args.country.lower()]
    if args.priority:
        filtered = [t for t in filtered if t["priority"].upper() == args.priority.upper()]
    if args.has_email:
        filtered = [t for t in filtered if t["email"]]
    if args.has_portal:
        filtered = [t for t in filtered if t["partner_page"]]
        
    print(f"\nFound {len(filtered)} institutions matching filters:")
    print("-" * 105)
    print(f"{'ID':<8} | {'Priority':<4} | {'Country':<12} | {'Institution Name':<38} | {'Status':<14} | {'Email / Contact':<20}")
    print("-" * 105)
    
    for t in filtered[:args.limit]:
        curr_status = status_dict.get(t["id"], {}).get("status", "IDENTIFIED")
        email_disp = t["email"] if t["email"] else ("Portal Link" if t["partner_page"] else "Research")
        name_disp = (t["name"][:35] + "..") if len(t["name"]) > 37 else t["name"]
        print(f"{t['id']:<8} | {t['priority']:<4} | {t['country']:<12} | {name_disp:<38} | {curr_status:<14} | {email_disp:<20}")
        
    if len(filtered) > args.limit:
        print(f"\n... and {len(filtered) - args.limit} more institutions. (Use --limit to view more)")
    print("-" * 105 + "\n")

def search_targets(args):
    targets = load_targets()
    query = args.query.lower()
    matches = []
    
    for t in targets:
        match_str = f"{t['name']} {t['country']} {t['state_or_city']} {t['programs']} {t['next_action']}".lower()
        if query in match_str:
            matches.append(t)
            
    print(f"\nSearch results for '{args.query}': ({len(matches)} matches)")
    print("-" * 105)
    for t in matches[:25]:
        print(f"[{t['id']}] {t['name']} ({t['country']}) - P: {t['priority']} - Email: {t['email'] or 'None'} - Portal: {t['partner_page'][:40] if t['partner_page'] else 'None'}")
    print("-" * 105 + "\n")

def generate_draft(args):
    targets = load_targets()
    target = None
    
    if args.id:
        for t in targets:
            if t["id"].lower() == args.id.lower():
                target = t
                break
    elif args.name:
        for t in targets:
            if args.name.lower() in t["name"].lower():
                target = t
                break
                
    if not target:
        print(f"Error: Target institution not found.", file=sys.stderr)
        return

    recipient_email = target["email"] or "[Admissions & Recruitment Office Email]"
    univ_name = target["name"]
    country = target["country"]
    programs = target["programs"] or "Undergraduate and Postgraduate STEM degree programs"
    portal = target["partner_page"] or target["website"]

    template_type = args.template.lower()
    
    if template_type == "direct":
        subject = f"Prospective Partnership: OpenSTEM Student Recruitment & STEM Pipeline from Bangladesh ({univ_name})"
        body = f"""Dear Admissions & International Recruitment Directorate,

I hope this email finds you well.

I am writing on behalf of OpenSTEM (https://openstemrecruitment.com/) to inquire about the procedure for establishing a formal international student recruitment partnership with {univ_name}.

OpenSTEM is an integrated STEM education, digital research preparatory, and university placement network headquartered in Dhaka, Bangladesh. Rather than operating as an unspecialized commercial agency, OpenSTEM maintains an active ecosystem of open digital learning and research platforms:
- OpenSTEM Lab (https://openstemlab.org/): Interactive virtual science and engineering simulations.
- OpenSTEM Replicate (https://openstemreplicate.org/): Scientific reproducibility and student research paper replication.
- OpenSTEM Library (https://openstemlibrary.com/): Curated open-access academic literature for STEM scholars.

Our Student Quality & Institutional Safeguards for {univ_name}:
1. Rigorous Academic Screening: We pre-screen candidates in mathematics, computing, and natural sciences, ensuring students meet your published entry criteria for programs such as {programs}.
2. Genuine Student (GS) Compliance: Complete independent verification of educational transcripts, standardized English scores (IELTS/TOEFL/PTE), and authentic financial sponsorship before any application is lodged.
3. Ethical Governance: OpenSTEM adheres strictly to international recruitment standards (including British Council AQF and AIRC principles) with zero student placement charges and zero document falsification tolerance.

We have prepared our formal 2-page Institutional Information Profile (detailing organization credentials, primary correspondent Shahriyar Karim, and independent domain verification mechanisms) for your administrative review.

Could you please advise on your partner onboarding schedule and provide your international representative application questionnaire? We would also welcome a 15-minute introductory video call at your convenience.

Thank you very much for your time and guidance.

Warm regards,

Shahriyar Karim
Founder & Managing Director | OpenSTEM
Recruitment Portal: https://openstemrecruitment.com/
Ecosystem Network: https://openstemlab.org/ | https://openstemlibrary.com/
Direct Correspondence: openstemrecruitment@gmail.com | shahriyarkarimsiam@gmail.com
"""

    elif template_type == "followup":
        subject = f"Re: Prospective Partnership: OpenSTEM Student Recruitment & STEM Pipeline from Bangladesh ({univ_name})"
        body = f"""Dear International Recruitment Team,

I am following up on our previous inquiry regarding an authorized international student recruitment partnership between {univ_name} and OpenSTEM (https://openstemrecruitment.com/).

As we advise high-achieving Bangladeshi students preparing applications for upcoming intakes, our academic counselors have identified strong student interest in {univ_name}'s academic degree offerings.

Through our educational platforms (OpenSTEM Lab and OpenSTEM Library), our candidates develop hands-on computational intuition and verified academic intent before submitting university documents, minimizing visa compliance risks and post-arrival attrition.

Could you kindly let us know if your international office is currently reviewing prospective agency agreements or if you require us to complete a specific portal questionnaire?

Thank you once again for your guidance.

Warm regards,

Shahriyar Karim
Founder & Managing Director | OpenSTEM
Email: openstemrecruitment@gmail.com
https://openstemrecruitment.com/
"""

    elif template_type == "faculty":
        subject = f"STEM Student Pathway & Research Bridge Collaboration: {univ_name} / OpenSTEM"
        body = f"""Dear Faculty Leadership & International Engagement Officers,

I am writing to explore an academic collaboration between {univ_name} and OpenSTEM (https://openstemrecruitment.com/).

OpenSTEM is an open digital education initiative in South Asia that builds virtual laboratories (openstemlab.org), computational tools (openstemtool.org), and academic literature platforms (openstemlibrary.com) to prepare secondary and undergraduate students for rigorous international STEM curricula.

We are actively mentoring Bangladeshi students pursuing degrees in Computer Science, Data Science, and Engineering. We would welcome the opportunity to:
1. Introduce {univ_name}'s degree programs to our pre-screened student cohorts.
2. Establish a direct academic progression pathway via our OpenSTEM Bridge platform (https://www.openstembridge.space/).
3. Host a joint virtual seminar connecting your faculty admissions leads directly with qualified candidates.

We would be delighted to schedule a brief introductory discussion.

Respectfully yours,

Shahriyar Karim
Founder & Director | OpenSTEM
https://openstemrecruitment.com/
openstemrecruitment@gmail.com
"""
    else:
        print(f"Unknown template: {template_type}")
        return

    output = f"""================================================================================
INSTITUTION: {univ_name} ({country})
TARGET ID:   {target['id']}
PRIORITY:    {target['priority']}
TO EMAIL:    {recipient_email}
PORTAL / URL:{portal}
SUBJECT:     {subject}
================================================================================

{body}
================================================================================
"""
    print(output)
    
    if args.save:
        filename = f"{target['id']}_{univ_name.replace(' ', '_')[:25]}.txt"
        filepath = os.path.join(DRAFTS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Draft saved to: {filepath}\n")

def mark_status(args):
    targets = load_targets()
    target = None
    for t in targets:
        if t["id"].lower() == args.id.lower():
            target = t
            break
            
    if not target:
        print(f"Error: Target ID '{args.id}' not found.", file=sys.stderr)
        return
        
    status_dict = load_status()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    status_dict[target["id"]] = {
        "name": target["name"],
        "country": target["country"],
        "status": args.status.upper(),
        "notes": args.notes or "",
        "updated_at": now_str
    }
    
    save_status(status_dict)
    print(f"\nUpdated {target['name']} [{target['id']}] to status: {args.status.upper()} (Notes: {args.notes or 'None'})\n")

def show_status(args):
    status_dict = load_status()
    targets = load_targets()
    
    stages = ["IDENTIFIED", "CONTACTED", "FORM_SUBMITTED", "IN_REVIEW", "AGREEMENT_RECEIVED", "SIGNED", "ON_HOLD"]
    counts = {s: 0 for s in stages}
    
    for t in targets:
        s = status_dict.get(t["id"], {}).get("status", "IDENTIFIED")
        if s in counts:
            counts[s] += 1
        else:
            counts["IDENTIFIED"] += 1
            
    total = len(targets)
    print("\n" + "="*50)
    print(" OPENSTEM PARTNERSHIP FUNNEL STATUS")
    print("="*50)
    for s in stages:
        pct = (counts[s] / total) * 100 if total > 0 else 0
        bar = "█" * int(pct // 2)
        print(f"{s:<20} | {counts[s]:<5} ({pct:>5.1f}%) | {bar}")
    print("="*50 + "\n")

def check_followups(args):
    status_dict = load_status()
    targets = load_targets()
    target_map = {t["id"]: t for t in targets}
    
    now = datetime.now()
    due_fu1 = []
    due_fu2 = []
    due_fu3 = []
    
    for tid, data in status_dict.items():
        if data.get("status") == "CONTACTED":
            updated_str = data.get("updated_at")
            if not updated_str:
                continue
            try:
                contacted_date = datetime.strptime(updated_str, "%Y-%m-%d %H:%M")
            except Exception:
                try:
                    contacted_date = datetime.strptime(updated_str.split()[0], "%Y-%m-%d")
                except Exception:
                    continue
            delta_days = (now - contacted_date).days
            target_info = target_map.get(tid, {})
            record = {
                "id": tid,
                "name": data.get("name") or target_info.get("name", "Unknown"),
                "email": target_info.get("email", ""),
                "country": data.get("country") or target_info.get("country", ""),
                "days": delta_days,
                "date": updated_str
            }
            if 5 <= delta_days < 12:
                due_fu1.append(record)
            elif 12 <= delta_days < 20:
                due_fu2.append(record)
            elif delta_days >= 20:
                due_fu3.append(record)
                
    print("\n" + "="*85)
    print(" OPENSTEM AUTOMATED FOLLOW-UP MONITOR")
    print("="*85)
    print(f"Follow-up #1 Due (5–11 days since contact): {len(due_fu1)}")
    for r in due_fu1:
        print(f"  • [{r['id']}] {r['name']} ({r['country']}) - {r['days']} days ago | Email: {r['email']}")
        
    print(f"\nFollow-up #2 Due (12–19 days since contact): {len(due_fu2)}")
    for r in due_fu2:
        print(f"  • [{r['id']}] {r['name']} ({r['country']}) - {r['days']} days ago | Email: {r['email']}")
        
    print(f"\nFollow-up #3 / Breakup Due (20+ days since contact): {len(due_fu3)}")
    for r in due_fu3:
        print(f"  • [{r['id']}] {r['name']} ({r['country']}) - {r['days']} days ago | Email: {r['email']}")
    print("="*85 + "\n")

def export_batch(args):
    targets = load_targets()
    filtered = targets
    if args.country:
        filtered = [t for t in filtered if t["country"].lower() == args.country.lower()]
    if args.priority:
        filtered = [t for t in filtered if t["priority"].upper() == args.priority.upper()]
    if args.has_email:
        filtered = [t for t in filtered if t["email"]]
        
    out_file = args.output or os.path.join(DATA_DIR, f"batch_{args.country or 'all'}_{args.priority or 'all'}.csv")
    fieldnames = ["id", "name", "country", "priority", "email", "partner_page", "website", "programs", "next_action"]
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(filtered)
    print(f"\nExported {len(filtered)} institutions to: {out_file}\n")

def main():
    parser = argparse.ArgumentParser(description="OpenSTEM University Outreach Pipeline Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # summary
    subparsers.add_parser("summary", help="Print overall pipeline metrics across all 15 countries")
    
    # list
    list_p = subparsers.add_parser("list", help="List and filter university targets")
    list_p.add_argument("--country", type=str, help="Filter by country (e.g. USA, UK, Canada, Australia)")
    list_p.add_argument("--priority", type=str, help="Filter by priority (P1, P2, P3)")
    list_p.add_argument("--has-email", action="store_true", help="Only show institutions with verified email")
    list_p.add_argument("--has-portal", action="store_true", help="Only show institutions with partner application page")
    list_p.add_argument("--limit", type=int, default=20, help="Max records to display (default 20)")
    
    # search
    search_p = subparsers.add_parser("search", help="Search institutions by keyword")
    search_p.add_argument("query", type=str, help="Search string")
    
    # draft
    draft_p = subparsers.add_parser("draft", help="Generate a customized email draft")
    draft_p.add_argument("--id", type=str, help="Target institution ID (e.g. USA-004)")
    draft_p.add_argument("--name", type=str, help="Target institution name search")
    draft_p.add_argument("--template", type=str, default="direct", choices=["direct", "followup", "faculty"], help="Template type")
    draft_p.add_argument("--save", action="store_true", help="Save draft to file in drafts/ directory")
    
    # mark
    mark_p = subparsers.add_parser("mark", help="Update institution outreach status")
    mark_p.add_argument("--id", type=str, required=True, help="Target institution ID")
    mark_p.add_argument("--status", type=str, required=True, choices=["IDENTIFIED", "CONTACTED", "FORM_SUBMITTED", "IN_REVIEW", "AGREEMENT_RECEIVED", "SIGNED", "ON_HOLD"], help="New status")
    mark_p.add_argument("--notes", type=str, default="", help="Outreach notes / contact log")
    
    # status
    subparsers.add_parser("status", help="Show current pipeline stage funnel")
    
    # followups
    subparsers.add_parser("followups", help="Check which universities are due for follow-ups")
    
    # export-batch
    batch_p = subparsers.add_parser("export-batch", help="Export a filtered batch of targets to CSV")
    batch_p.add_argument("--country", type=str, help="Filter by country")
    batch_p.add_argument("--priority", type=str, help="Filter by priority")
    batch_p.add_argument("--has-email", action="store_true", help="Only include records with emails")
    batch_p.add_argument("--output", type=str, help="Output CSV path")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    if args.command == "summary":
        print_summary()
    elif args.command == "list":
        list_targets(args)
    elif args.command == "search":
        search_targets(args)
    elif args.command == "draft":
        generate_draft(args)
    elif args.command == "mark":
        mark_status(args)
    elif args.command == "status":
        show_status(args)
    elif args.command == "followups":
        check_followups(args)
    elif args.command == "export-batch":
        export_batch(args)

if __name__ == "__main__":
    main()
