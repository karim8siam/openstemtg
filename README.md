# OpenSTEM Global University Outreach & Partnership System
**Target:** 1,000+ Global Partner Universities Across 15 Countries  
**Lead Correspondent:** Shahriyar Karim  
**Primary Platform:** [openstemrecruitment.com](https://openstemrecruitment.com/)  
**Email:** `openstemrecruitment@gmail.com` | `shahriyarkarimsiam@gmail.com`  

---

## 📁 Workspace Directory Structure

```text
open stem university outreach/
├── docs/
│   ├── USA_6_MONTH_CAMPAIGN_PLAN.md        # Master 6-month operational plan dedicated to the USA
│   ├── STRATEGY_AND_ROADMAP.md             # Multi-year scaling blueprint from 0 to 1,000+ universities
│   ├── ECOSYSTEM_VALUE_PROPOSITION.md      # How the 6 sister platforms establish institutional trust
│   ├── COMPLIANCE_AND_DUE_DILIGENCE.md     # Trade license, tax ID roadmap, and pre-answered university FAQs
│   └── OUTREACH_PLAYBOOK_AND_TEMPLATES.md  # Multi-stage email sequences, follow-ups, and objections handling
├── tools/
│   ├── pipeline_manager.py                 # Core CLI for filtering leads, drafting pitches, and tracking status
│   └── export_targets.py                   # Data sync tool connecting to Google Sheet (1,134 records across 15 countries)
├── templates/
│   ├── 01_initial_enquiry_direct.txt       # Direct university cold pitch
│   ├── 02_pathway_aggregator_application.txt# Master pathway outreach (INTO, Shorelight, Kaplan, Navitas)
│   ├── 03_faculty_stem_bridge.txt          # Academic Dean / Faculty collaboration pitch
│   ├── 04_followup_value_add.txt           # Follow-up #1 (Day 4-5)
│   ├── 05_followup_compliance_pack.txt     # Follow-up #2 (Day 10-12)
│   └── 06_webform_portal_responses.txt     # Ready-to-copy fields for online agent application forms
├── data/
│   ├── targets.json                        # 1,134 normalized university records
│   ├── targets.csv                         # Master spreadsheet export
│   ├── country_summary.json                # Statistical breakdown across all 15 countries
│   └── pipeline_status.json                # Active tracking database for outreach stages
└── drafts/                                 # Generated, personalized emails ready for sending
```

---

## 🚀 Quick Start Guide

### 1. View Pipeline Summary Across All 15 Countries
```bash
python3 tools/pipeline_manager.py summary
```

### 2. Find Priority 1 Targets with Direct Emails
```bash
# View Priority 1 targets in the USA with verified contact emails
python3 tools/pipeline_manager.py list --country USA --priority P1 --has-email --limit 10

# View Priority 1 targets in the UK
python3 tools/pipeline_manager.py list --country UK --priority P1 --has-email
```

### 3. Generate a Personalized Email Draft for Any University
```bash
# Generate draft by ID and save to drafts/ folder
python3 tools/pipeline_manager.py draft --id USA-004 --save

# Generate draft by university name
python3 tools/pipeline_manager.py draft --name "Brandon University" --save
```

### 4. Update Outreach Status in the Pipeline
```bash
# Mark as Contacted
python3 tools/pipeline_manager.py mark --id USA-004 --status CONTACTED --notes "Sent initial outreach with Institutional Profile"

# Mark as Form Submitted
python3 tools/pipeline_manager.py mark --id USA-001 --status FORM_SUBMITTED --notes "Submitted online agent application form"
```

### 5. Check Overall Outreach Funnel Progress
```bash
python3 tools/pipeline_manager.py status
```

---

## 📑 Core Documentation Highlights

1. **[Master Strategy & Roadmap](docs/STRATEGY_AND_ROADMAP.md)**: The 3-route strategy (Direct, Pathway aggregators, and Academic MoUs) to reach 1,000+ universities, plus the 24-week timeline.
2. **[Ecosystem Value Proposition](docs/ECOSYSTEM_VALUE_PROPOSITION.md)**: Why universities care about OpenSTEM Library, Lab, Replicate, Tool, Field, and Bridge, and how this prevents visa fraud and student attrition.
3. **[Compliance & Due Diligence Dossier](docs/COMPLIANCE_AND_DUE_DILIGENCE.md)**: Standard answers for university vetting, the Institutional Information Profile submission, and the Bangladesh Trade License / e-TIN execution checklist.
4. **[Outreach Playbook & Templates](docs/OUTREACH_PLAYBOOK_AND_TEMPLATES.md)**: Word-for-word email sequences, follow-ups, and winning responses to common university objections.
