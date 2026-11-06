import html
import math
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.db import search_opportunities
from bot.config import LEAD_EMAIL, TELEGRAM_CHANNEL
from bot.keyboards import (
    get_subjects_keyboard,
    get_countries_keyboard,
    get_opportunities_view_keyboard,
    EXPLORE_WEB_URL,
)

PAGE_SIZE = 3

SUBJECT_NAMES = {
    "computer-science": "Computer Science",
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

def format_opportunity_card(opp):
    title = html.escape(opp.get("title") or "Opportunity")
    university = html.escape(opp.get("university") or "N/A")
    country = html.escape(opp.get("country") or "Global")
    opp_type = html.escape(opp.get("type") or "Program")
    funding = html.escape(opp.get("funding") or "See official link")
    deadline = html.escape(opp.get("deadline") or "Rolling / Unspecified")
    gpa = html.escape(opp.get("gpa") or "")
    ielts = html.escape(opp.get("ielts") or "")
    gre = html.escape(opp.get("gre") or "")
    source = opp.get("source") or EXPLORE_WEB_URL
    
    card = f"🎓 <b>{title}</b>\n"
    card += f"🏛️ <b>Institution:</b> {university} (📍 {country})\n"
    card += f"🏷️ <b>Type:</b> {opp_type}\n"
    card += f"💰 <b>Funding:</b> {funding}\n"
    card += f"⏰ <b>Deadline:</b> <code>{deadline}</code>\n"
    
    reqs = []
    if gpa:
        reqs.append(f"GPA: {gpa[:35]}")
    if ielts:
        reqs.append(f"IELTS: {ielts[:30]}")
    if gre:
        reqs.append(f"GRE: {gre[:25]}")
    if reqs:
        card += f"📋 <b>Requirements:</b> {', '.join(reqs)}\n"

    card += f"🔗 <a href='{html.escape(source)}'>Official University Link ↗</a>\n"
    card += f"📢 <b>Updates Channel:</b> <a href='{TELEGRAM_CHANNEL}'>OpenSTEM (@openstemedu)</a>\n"
    card += f"✉️ <b>Admissions Guidance:</b> <code>{LEAD_EMAIL}</code>"
    return card

async def start_opportunity_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎓 <b>Explore Your Opportunity</b>\n"
        "<i>Explore source-linked program details and graduate funding information across 11,000+ listings.</i>\n\n"
        "👇 <b>Step 1: Choose your STEM Subject</b> (or select All Subjects):"
    )
    reply_markup = get_subjects_keyboard()
    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception:
            await update.callback_query.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)

async def subject_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data.replace("sel_sub_", "")
    context.user_data["selected_subject"] = subject
    subject_label = SUBJECT_NAMES.get(subject, subject.title())

    text = (
        f"🎓 <b>Subject:</b> <code>{subject_label}</code>\n\n"
        f"👇 <b>Step 2: Choose Country</b> (or select All Countries):"
    )
    await query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=get_countries_keyboard(), disable_web_page_preview=True)

async def step_change_country_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = context.user_data.get("selected_subject", "all")
    subject_label = SUBJECT_NAMES.get(subject, subject.title())
    text = (
        f"🎓 <b>Subject:</b> <code>{subject_label}</code>\n\n"
        f"👇 <b>Step 2: Choose Country</b> (or select All Countries):"
    )
    await query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=get_countries_keyboard(), disable_web_page_preview=True)

async def country_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data.replace("sel_cnt_", "")
    context.user_data["selected_country"] = country
    context.user_data["selected_type"] = "all"
    context.user_data["current_page"] = 0
    await render_opportunity_results(query.message, context, is_edit=True)

async def type_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    opp_type = query.data.replace("sel_typ_", "")
    context.user_data["selected_type"] = opp_type
    context.user_data["current_page"] = 0
    await render_opportunity_results(query.message, context, is_edit=True)

async def opp_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = int(query.data.replace("opp_page_", ""))
    context.user_data["current_page"] = page
    await render_opportunity_results(query.message, context, is_edit=True)

async def render_opportunity_results(message, context, is_edit=True):
    subject = context.user_data.get("selected_subject", "all")
    country = context.user_data.get("selected_country", "all")
    opp_type = context.user_data.get("selected_type", "all")
    page = context.user_data.get("current_page", 0)

    offset = page * PAGE_SIZE
    rows, total_count = search_opportunities(
        subject=subject,
        country=country,
        opp_type=opp_type,
        limit=PAGE_SIZE,
        offset=offset
    )

    subject_label = SUBJECT_NAMES.get(subject, subject.title())
    country_label = country.title() if country != "all" else "All Countries"
    type_label = opp_type.title() if opp_type != "all" else "All Types"

    if total_count == 0:
        no_res_text = (
            f"⚠️ <b>No matching opportunities found.</b>\n\n"
            f"📚 <b>Subject:</b> {subject_label}\n"
            f"📍 <b>Country:</b> {country_label}\n"
            f"🏷️ <b>Type:</b> {type_label}\n\n"
            f"Try selecting a different filter or view all opportunities on the website:"
        )
        keyboard = [
            [
                InlineKeyboardButton("🌍 Change Country", callback_data="step_change_country"),
                InlineKeyboardButton("📚 Change Subject", callback_data="open_opp_start"),
            ],
            [
                InlineKeyboardButton("🔗 Explore on Web (openstemfield.org) ↗", url=EXPLORE_WEB_URL)
            ],
            [
                InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if is_edit:
            try:
                await message.edit_text(no_res_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
            except Exception:
                await message.reply_text(no_res_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        else:
            await message.reply_text(no_res_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        return

    total_pages = max(1, math.ceil(total_count / PAGE_SIZE))

    header = (
        f"🌟 <b>OpenSTEM Opportunities</b> (Found {total_count:,})\n"
        f"📚 <b>Subject:</b> {subject_label} | 📍 <b>Country:</b> {country_label}\n"
        f"🏷️ <b>Type:</b> {type_label} | 📄 <b>Page:</b> {page + 1}/{total_pages}\n\n"
        f"<i>Select an opportunity type below to filter further:</i>\n\n"
    )

    cards = [format_opportunity_card(r) for r in rows]
    full_text = header + "\n" + "—" * 22 + "\n\n" + "\n\n".join(cards)

    reply_markup = get_opportunities_view_keyboard(total_pages, page, current_type=opp_type)

    if is_edit:
        try:
            await message.edit_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception:
            await message.reply_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
    else:
        await message.reply_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
