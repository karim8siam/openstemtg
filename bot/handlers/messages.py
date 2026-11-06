from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.handlers.start import (
    explore_openstem_handler,
    contact_handler,
    community_handler,
    mentorship_handler,
)
from bot.handlers.opportunities import (
    show_opportunities_menu,
    render_opportunities_list,
    format_opportunity_card,
)
from bot.handlers.professors import (
    show_professors_menu,
    render_professors_list,
    format_professor_card,
)
from bot.db import search_opportunities, search_researchers
import html

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    # Reply keyboard navigation
    if "1. Explore OpenSTEM" in text or "Explore OpenSTEM" in text:
        await explore_openstem_handler(update, context)
        return
    elif "Search Opportunities" in text:
        await show_opportunities_menu(update, context)
        return
    elif "Find STEM Professors" in text:
        await show_professors_menu(update, context)
        return
    elif "Free Mentorship & Help" in text:
        await mentorship_handler(update, context)
        return
    elif "Student Community" in text:
        await community_handler(update, context)
        return
    elif "Contact Us" in text:
        await contact_handler(update, context)
        return

    # Check state for custom search
    if context.user_data.get("waiting_for_opp_search"):
        context.user_data["waiting_for_opp_search"] = False
        context.user_data["opp_current_query"] = text
        context.user_data["opp_current_type"] = None
        context.user_data["opp_current_country"] = None
        await render_opportunities_list(update.message, context, search_q=text, page=0, is_edit=False)
        return

    if context.user_data.get("waiting_for_prof_search"):
        context.user_data["waiting_for_prof_search"] = False
        context.user_data["prof_current_query"] = text
        context.user_data["prof_current_subject"] = None
        await render_professors_list(update.message, context, search_q=text, page=0, is_edit=False)
        return

    # Default fallback: Treat as opportunity search query
    context.user_data["opp_current_query"] = text
    context.user_data["opp_current_type"] = None
    context.user_data["opp_current_country"] = None
    await render_opportunities_list(update.message, context, search_q=text, page=0, is_edit=False)

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        return

    results = []
    # Search opportunities
    opps, _ = search_opportunities(query=query, limit=10)
    for o in opps:
        card = format_opportunity_card(o)
        title = f"🎓 {o.get('title')} ({o.get('country')})"
        desc = f"{o.get('university')} | {o.get('funding', '')[:60]}"
        results.append(
            InlineQueryResultArticle(
                id=f"opp_{o['id']}",
                title=title,
                description=desc,
                input_message_content=InputTextMessageContent(
                    message_text=card,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            )
        )

    # Search researchers
    profs, _ = search_researchers(query=query, limit=5)
    for p in profs:
        card = format_professor_card(p)
        title = f"👨‍🔬 {p.get('name')} - {p.get('university')}"
        desc = f"{p.get('title')} | Topics: {p.get('topics', '')[:60]}"
        results.append(
            InlineQueryResultArticle(
                id=f"prof_{p['id']}",
                title=title,
                description=desc,
                input_message_content=InputTextMessageContent(
                    message_text=card,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            )
        )

    await update.inline_query.answer(results[:20], cache_time=10)
