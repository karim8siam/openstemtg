from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.config import LEAD_EMAIL

STUDENTS_WEB_URL = "https://openstemrecruitment.com/students.html"
GMAIL_STUDENT_HELP_URL = f"https://mail.google.com/mail/?view=cm&fs=1&to={LEAD_EMAIL}&su=Student%20Support%20%26%20Guidance%20Inquiry"

HOW_HELP_TEXT = f"""
🤝 <b>How OpenSTEM Will Help You</b>
<i>Explore 14 dedicated support areas designed to guide your international STEM education and research journey.</i>

<b>🔍 1. DISCOVER (Exploring Opportunities)</b>
• <b>01. Initial study conversation:</b> Clarify your academic goals, study level, time frame, and budget before choosing a direction.
• <b>02. Academic eligibility review:</b> Compare your academic qualifications with current, official university entry requirements.
• <b>03. Scholarship &amp; funding discovery:</b> Find verified funding opportunities and examine eligibility, award coverage, and deadlines.
• <b>04. University &amp; program shortlisting:</b> Compare subject fit, accreditation, realistic costs, and application rules.

<b>🤝 2. CONNECT (Research &amp; Professors)</b>
• <b>05. Research opportunity discovery:</b> Explore published funded PhD positions and research roles through legitimate sources.
• <b>06. Professor &amp; research group research:</b> Identify faculty research interests and prepare evidence-based, respectful academic outreach.
• <b>07. Peer-learning community:</b> Engage in study discussions and academic collaboration through the wider OpenSTEM community.

<b>📝 3. PREPARE (Application &amp; Readiness)</b>
• <b>08. Academic CV &amp; statement feedback:</b> Improve the structure and clarity of your CV, statement of purpose (SOP), or research proposal.
• <b>09. Application planning &amp; checks:</b> Organize required documents, official requirements, and timelines to prevent avoidable mistakes.
• <b>10. Research-readiness planning:</b> Identify research methods, subject literature, and project skills worth strengthening.
• <b>11. Academic portfolio guidance:</b> Present genuine STEM projects, computational code, and academic work clearly.
• <b>12. Interview practice:</b> Prepare to explain your academic motivations, research interests, and experiences with confidence.
• <b>13. Student workshops &amp; explainers:</b> Structured sessions covering application steps, funding roadmaps, and academic preparation.

<b>✈️ 4. TRANSITION (Arrival &amp; Enrolment)</b>
• <b>14. Pre-departure information:</b> Locate official enrolment, arrival, and orientation checklists for your target university.

—
✉️ <b>Direct Advisor Email:</b> <code>{LEAD_EMAIL}</code>
🎓 <b>Recruitment Platform:</b> <a href="{STUDENTS_WEB_URL}">openstemrecruitment.com/students</a>

<i>Have questions about any of these 14 support areas? Tap the button below to email directly!</i>
"""

def get_how_help_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎓 View on Recruitment Website ↗", url=STUDENTS_WEB_URL)
        ],
        [
            InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_STUDENT_HELP_URL)
        ],
        [
            InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main")
        ]
    ])

async def how_openstem_helps_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_how_help_keyboard()
    if update.message:
        await update.message.reply_text(
            HOW_HELP_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(
                HOW_HELP_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        except Exception:
            await update.callback_query.message.reply_text(
                HOW_HELP_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
