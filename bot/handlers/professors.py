import html
import math
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.db import search_researchers
from bot.keyboards import (
    get_professors_subject_keyboard,
    get_professors_view_keyboard,
    COUNTRY_FLAGS,
    BRIDGE_URL,
    GMAIL_RESEARCH_URL,
)
from bot.config import LEAD_EMAIL

PROF_PAGE_SIZE = 3

PROF_SUBJECT_LABELS = {
    "computer-science": "Computer Science & AI",
    "engineering": "Engineering",
    "physics": "Physics",
    "mathematics": "Mathematics",
    "biology": "Biology & Medicine",
    "chemistry": "Chemistry",
    "environment": "Earth & Environment",
    "social-sciences": "Social Sciences",
    "arts-design": "Arts & Design",
    "all": "All Subjects",
}

def format_professor_card(prof):
    name = html.escape(prof.get("name") or "Professor")
    title = html.escape(prof.get("title") or "Faculty Researcher")
    university = html.escape(prof.get("university") or "University")
    country = html.escape(prof.get("country") or "")
    email = prof.get("email") or ""
    topics = html.escape(prof.get("topics") or "")
    summary = html.escape(prof.get("summary") or "")
    source = prof.get("source") or ""

    flag = COUNTRY_FLAGS.get(country, "🏛️")
    location = f"{university} ({flag} {country})" if country else university

    card = f"👨‍🔬 <b>{name}</b>\n"
    card += f"🎖️ <b>Title:</b> {title}\n"
    card += f"🏛️ <b>Institution:</b> {location}\n"
    if topics:
        card += f"🔬 <b>Research Field / Topics:</b> {topics}\n"
    if summary:
        card += f"📝 <b>Lab Focus:</b> <i>{summary[:150]}...</i>\n"
    if email:
        card += f"📧 <b>Faculty Email:</b> <code>{html.escape(email)}</code>\n"
    if source:
        card += f"🔗 <a href='{html.escape(source)}'>Official Faculty Profile ↗</a>\n"
    card += f"✉️ <b>Direct Advisor Contact:</b> <code>{LEAD_EMAIL}</code>\n"
    card += f"🌉 <b>OpenSTEM Bridge:</b> <a href='{BRIDGE_URL}'>openstembridge.space ↗</a>"
    return card

async def start_professors_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔬 <b>Explore Professor for Perfect Research</b>\n"
        "<i>Discover 5,090+ professors and principal investigators leading research labs worldwide across all major STEM disciplines.</i>\n\n"
        f"✉️ <b>Direct Advisor Email:</b> <code>{LEAD_EMAIL}</code>\n"
        f"🌉 <b>Research Mentorship &amp; Bridge:</b> <a href='{BRIDGE_URL}'>openstembridge.space ↗</a>\n\n"
        "👇 <b>Select a Subject to view professors:</b>"
    )
    reply_markup = get_professors_subject_keyboard()

    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception:
            await update.callback_query.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)

async def prof_subject_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data.replace("p_sub_", "")
    context.user_data["prof_subject"] = subject
    context.user_data["prof_page"] = 0
    await render_professors_results(query.message, context, is_edit=True)

async def prof_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = int(query.data.replace("p_page_", ""))
    context.user_data["prof_page"] = page
    await render_professors_results(query.message, context, is_edit=True)

async def render_professors_results(message, context, is_edit=True):
    subject = context.user_data.get("prof_subject", "all")
    page = context.user_data.get("prof_page", 0)

    offset = page * PROF_PAGE_SIZE
    rows, total_count = search_researchers(
        subject=subject,
        limit=PROF_PAGE_SIZE,
        offset=offset
    )

    subject_label = PROF_SUBJECT_LABELS.get(subject, subject.title())
    total_pages = max(1, math.ceil(total_count / PROF_PAGE_SIZE))

    header = (
        f"🔬 <b>Professors in {subject_label}</b> ({total_count:,} Faculty)\n"
        f"<i>Connect with researchers for thesis supervision, funded lab assistantships, or research collaboration.</i>\n"
        f"✉️ <b>Advisor Email:</b> <code>{LEAD_EMAIL}</code> | 🌉 <b>Bridge:</b> <a href='{BRIDGE_URL}'>openstembridge.space ↗</a>\n"
        f"📄 <b>Page:</b> {page + 1}/{total_pages}\n\n"
    )

    cards = [format_professor_card(r) for r in rows]
    full_text = header + ("—" * 22) + "\n\n" + "\n\n".join(cards)

    reply_markup = get_professors_view_keyboard(total_pages, page)

    if is_edit:
        try:
            await message.edit_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception:
            await message.reply_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
    else:
        await message.reply_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
