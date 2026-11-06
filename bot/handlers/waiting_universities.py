import html
import math
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.db import (
    get_waiting_university_countries,
    get_waiting_universities_by_country,
)
from bot.keyboards import (
    get_waiting_countries_keyboard,
    get_waiting_universities_view_keyboard,
    COUNTRY_FLAGS,
    RECRUITMENT_URL,
)
from bot.config import LEAD_EMAIL

WAITING_PAGE_SIZE = 3

def format_waiting_university_card(uni):
    name = html.escape(uni.get("name") or "University")
    country = html.escape(uni.get("country") or "Global")
    state_or_city = html.escape(uni.get("state_or_city") or "")
    url = uni.get("url") or RECRUITMENT_URL
    programs = html.escape(uni.get("programs") or "Undergraduate & Graduate STEM Pathways")
    flag = COUNTRY_FLAGS.get(uni.get("country"), "🏛️")

    location_str = f"{state_or_city}, {country}" if state_or_city else country

    card = f"{flag} <b>{name}</b>\n"
    card += f"📍 <b>Location:</b> {location_str}\n"
    card += f"📋 <b>Directory status:</b> <i>Research listing; not a confirmed OpenSTEM partnership</i>\n"
    if programs:
        card += f"📚 <b>Focus &amp; Pathways:</b> {programs[:150]}\n"
    card += f"🔗 <a href='{html.escape(url)}'>Official University Portal ↗</a>\n"
    card += f"🎓 <b>Recruitment Platform:</b> <a href='{RECRUITMENT_URL}'>OpenSTEM Recruitment</a>\n"
    card += f"✉️ <b>Admissions Inquiry:</b> <code>{LEAD_EMAIL}</code>"
    return card

async def start_waiting_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country_counts = get_waiting_university_countries()
    total_unis = sum(cnt for _, cnt in country_counts)

    text = (
        f"🏛️ <b>Explore Your Waiting Universities</b>\n"
        f"<i>Browse over {total_unis:,} institutions across 15 countries. These are university directory listings for research. Inclusion does not imply an OpenSTEM partnership or guarantee current admissions availability.</i>\n\n"
        f"👇 <b>Select a Country to see universities:</b>"
    )
    reply_markup = get_waiting_countries_keyboard(country_counts)

    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception:
            await update.callback_query.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)

async def waiting_country_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data.replace("w_cnt_", "")
    context.user_data["waiting_country"] = country
    context.user_data["waiting_page"] = 0
    await render_waiting_universities_results(query.message, context, is_edit=True)

async def waiting_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = int(query.data.replace("w_page_", ""))
    context.user_data["waiting_page"] = page
    await render_waiting_universities_results(query.message, context, is_edit=True)

async def render_waiting_universities_results(message, context, is_edit=True):
    country = context.user_data.get("waiting_country", "all")
    page = context.user_data.get("waiting_page", 0)

    offset = page * WAITING_PAGE_SIZE
    rows, total_count = get_waiting_universities_by_country(
        country=country,
        limit=WAITING_PAGE_SIZE,
        offset=offset
    )

    flag = COUNTRY_FLAGS.get(country, "🌍")
    country_label = country if country != "all" else "All Countries"
    total_pages = max(1, math.ceil(total_count / WAITING_PAGE_SIZE))

    header = (
        f"🏛️ <b>Waiting Universities in {flag} {country_label}</b> ({total_count:,} Institutions)\n"
        f"<i>Verify current programs and admissions availability on each university’s official website.</i>\n"
        f"📄 <b>Page:</b> {page + 1}/{total_pages}\n\n"
    )

    cards = [format_waiting_university_card(r) for r in rows]
    full_text = header + ("—" * 22) + "\n\n" + "\n\n".join(cards)

    reply_markup = get_waiting_universities_view_keyboard(total_pages, page)

    if is_edit:
        try:
            await message.edit_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception:
            await message.reply_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
    else:
        await message.reply_text(full_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)
