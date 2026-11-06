from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.config import LEAD_EMAIL, URLS

YOUTUBE_URL = URLS["youtube"]
GMAIL_COURSES_URL = f"https://mail.google.com/mail/?view=cm&fs=1&to={LEAD_EMAIL}&su=Free%20Courses%20%26%20Test%20Preparation%20Inquiry"

COURSES_TEXT = f"""
🎓 <b>Free Courses &amp; Test Preparation</b>
<i>By OpenSTEM Bangladesh — 100% Free Learning &amp; Study Abroad Prep.</i>

Get fully prepared for international admissions, standardized tests, and professor recommendations with our free video lectures and roadmaps.

<b>📚 Preparation Areas Available:</b>
• <b>🇬🇧 IELTS Preparation:</b> Band 7.5+ strategies, academic reading, writing task 1 &amp; 2, and speaking practice.
• <b>🇺🇸 GRE Preparation:</b> High-scoring quantitative math tricks, verbal vocabulary, and analytical writing.
• <b>📝 SAT Preparation:</b> Digital SAT math, reading, and writing modules for top undergraduate scholarships.
• <b>🎯 ACT Preparation:</b> Fast-paced test strategies, math, and science section scoring techniques.
• <b>📄 LOR Preparation:</b> How to draft, structure, and request winning Letters of Recommendation from professors.

📢 <b>Notice on Course Materials:</b>
If any specific course, video, or practice material is currently missing, do not worry! We are constantly recording and releasing new lessons. You will get them <b>completely free</b> on our YouTube channel (<b>OpenSTEM Bangladesh</b>) as soon as possible.

—
📺 <b>Official Channel:</b> <a href="{YOUTUBE_URL}">OpenSTEM Bangladesh on YouTube</a>
✉️ <b>Direct Advisor Email:</b> <code>{LEAD_EMAIL}</code>

<i>Tap any test button below to start learning on our YouTube channel:</i>
"""

def get_courses_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇬🇧 IELTS Preparation ↗", url=YOUTUBE_URL),
            InlineKeyboardButton("🇺🇸 GRE Preparation ↗", url=YOUTUBE_URL),
        ],
        [
            InlineKeyboardButton("📝 SAT Preparation ↗", url=YOUTUBE_URL),
            InlineKeyboardButton("🎯 ACT Preparation ↗", url=YOUTUBE_URL),
        ],
        [
            InlineKeyboardButton("📄 LOR (Recommendation Letters) ↗", url=YOUTUBE_URL),
        ],
        [
            InlineKeyboardButton("📺 Watch OpenSTEM Bangladesh on YouTube ↗", url=YOUTUBE_URL),
        ],
        [
            InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_COURSES_URL),
        ],
        [
            InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main"),
        ]
    ])

async def free_courses_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_courses_keyboard()
    if update.message:
        await update.message.reply_text(
            COURSES_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    elif update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.edit_text(
                COURSES_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        except Exception:
            await update.callback_query.message.reply_text(
                COURSES_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
