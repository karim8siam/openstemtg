from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.config import LEAD_EMAIL, URLS, TELEGRAM_CHANNEL

DISCORD_URL = URLS["discord"]
RECRUITMENT_URL = URLS["recruitment"]
GMAIL_PARTNER_URL = f"https://mail.google.com/mail/?view=cm&fs=1&to={LEAD_EMAIL}&su=OpenSTEM%20Partnership%20%26%20Collaboration%20Proposal"

PARTNERSHIP_TEXT = f"""
🤝 <b>Join the OpenSTEM Partnership Programme</b>
<i>Building bridges. Empowering minds. Creating life-changing opportunities.</i>

<blockquote><b>"Sometimes, a single meaningful connection can change the entire course of a life."</b></blockquote>

Great achievements in science, academia, and global education are never built in isolation. When passionate educators, researchers, institutional leaders, and mentors connect, invisible walls crumble — opening doors to world-class opportunities for ambitious students.

<b>🌟 Why Partner with OpenSTEM?</b>
• <b>Global STEM Reach:</b> Direct engagement with thousands of high-achieving students, future researchers, and scholars.
• <b>Research &amp; Lab Bridges:</b> Facilitating supervisor matching, funded lab placements, and thesis co-supervision.
• <b>Open-Access Synergy:</b> Collaborating across our 7 sister platforms (Field, Recruitment, Lab, Library, Tool, Bridge, Replicate).
• <b>Generational Impact:</b> Nurturing authentic STEM talent and breaking socioeconomic barriers in global higher education.

Whether you are a university representative, research professor, educational institution, or an enthusiastic student organization:

🚀 <b>Let's do a powerful partnership and shape the future together.</b>

—
📢 <b>Official Telegram Channel:</b> <a href="{TELEGRAM_CHANNEL}">OpenSTEM (@openstemedu)</a>
💬 <b>Discord Community:</b> <a href="{DISCORD_URL}">OpenSTEM Discord Server</a>
✉️ <b>Direct Contact for Partnership:</b> <code>{LEAD_EMAIL}</code>

<i>Tap below to email us your collaboration vision or proposal directly:</i>
"""

def get_partnership_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_PARTNER_URL),
        ],
        [
            InlineKeyboardButton("📢 OpenSTEM Channel ↗", url=TELEGRAM_CHANNEL),
            InlineKeyboardButton("💬 Discord Community ↗", url=DISCORD_URL),
        ],
        [
            InlineKeyboardButton("🎓 Recruitment Platform ↗", url=RECRUITMENT_URL),
        ],
        [
            InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main"),
        ]
    ])

async def partnership_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_partnership_keyboard()
    if update.message:
        await update.message.reply_text(
            PARTNERSHIP_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(
                PARTNERSHIP_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        except Exception:
            await update.callback_query.message.reply_text(
                PARTNERSHIP_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
