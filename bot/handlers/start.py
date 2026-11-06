from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.keyboards import (
    get_main_menu_keyboard,
    get_welcome_inline_keyboard,
    get_explore_openstem_keyboard,
)
from bot.config import LEAD_EMAIL, URLS

WELCOME_TEXT = """
✨ <b>Welcome to OpenSTEM Official Bot!</b> ✨
<i>Your student-first gateway to global STEM scholarships, graduate degrees, and academic funding.</i>

Choose an option below to begin:
"""

EXPLORE_OPENSTEM_TEXT = f"""
🌐 <b>Explore OpenSTEM</b>

Tap any button below to visit our platforms, social media, or email us directly:

<b>Websites:</b>
• <b>Field:</b> <a href="{URLS['field']}">openstemfield.org</a>
• <b>Recruitment:</b> <a href="{URLS['recruitment']}">openstemrecruitment.com</a>
• <b>Research / Lab:</b> <a href="{URLS['lab']}">openstemlab.org</a>
• <b>Book / Library:</b> <a href="{URLS['library']}">openstemlibrary.com</a>
• <b>Tool:</b> <a href="{URLS['tool']}">openstemtool.org</a>
• <b>Bridge:</b> <a href="{URLS['bridge']}">openstembridge.space</a>
• <b>Replicate:</b> <a href="{URLS['replicate']}">openstemreplicate.org</a>

<b>Social Media &amp; Community:</b>
• <b>YouTube:</b> <a href="{URLS['youtube']}">OpenSTEM YouTube Channel</a>
• <b>Facebook:</b> <a href="{URLS['facebook']}">OpenSTEM Facebook Page</a>
• <b>Discord:</b> <a href="{URLS['discord']}">OpenSTEM Discord Community</a>

<b>Direct Email:</b>
• <code>{LEAD_EMAIL}</code>
"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard(),
            disable_web_page_preview=True
        )

async def explore_openstem_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_explore_openstem_keyboard()
    if update.message:
        await update.message.reply_text(
            EXPLORE_OPENSTEM_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(
                EXPLORE_OPENSTEM_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        except Exception:
            await update.callback_query.message.reply_text(
                EXPLORE_OPENSTEM_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )

async def back_to_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.message.edit_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_welcome_inline_keyboard(),
            disable_web_page_preview=True
        )
    except Exception:
        await query.message.reply_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard(),
            disable_web_page_preview=True
        )
