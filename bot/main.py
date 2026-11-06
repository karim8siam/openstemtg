import logging
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

# Set root directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from bot.config import BOT_TOKEN
from bot.handlers.start import (
    start_command,
    explore_openstem_handler,
    back_to_main_callback,
)
from bot.handlers.opportunities import (
    start_opportunity_flow,
    subject_selected_callback,
    step_change_country_callback,
    country_selected_callback,
    type_selected_callback,
    opp_page_callback,
)
from bot.handlers.waiting_universities import (
    start_waiting_flow,
    waiting_country_selected_callback,
    waiting_page_callback,
)
from bot.handlers.professors import (
    start_professors_flow,
    prof_subject_selected_callback,
    prof_page_callback,
)
from bot.handlers.help_services import how_openstem_helps_handler
from bot.handlers.courses import free_courses_handler
from bot.handlers.partnership import partnership_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("OpenSTEM_Bot")

# Tiny HTTP server for free cloud keep-awake (Render, Koyeb, etc.)
class HealthServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OpenSTEM Telegram Bot is active and running 24/7!\n")

    def log_message(self, format, *args):
        pass

def start_health_server():
    preferred_port = int(os.environ.get("PORT", 8080))
    for port in [preferred_port, 8000, 8888, 5000, 0]:
        try:
            server = HTTPServer(("0.0.0.0", port), HealthServerHandler)
            actual_port = server.server_address[1]
            logger.info("Health check server active on port %s for 24/7 cloud keep-awake!", actual_port)
            server.serve_forever()
            break
        except OSError:
            continue

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "noop":
        await query.answer()
        return

    if data == "back_to_main":
        await back_to_main_callback(update, context)
        return

    if data == "open_explore":
        await explore_openstem_handler(update, context)
        return

    if data == "open_opp_start":
        await start_opportunity_flow(update, context)
        return

    if data == "open_waiting_start":
        await start_waiting_flow(update, context)
        return

    if data == "open_prof_start":
        await start_professors_flow(update, context)
        return

    if data == "open_how_help":
        await how_openstem_helps_handler(update, context)
        return

    if data == "open_courses_start":
        await free_courses_handler(update, context)
        return

    if data == "open_partnership_start":
        await partnership_handler(update, context)
        return

    # Opportunity filters
    if data == "step_change_country":
        await step_change_country_callback(update, context)
        return

    if data.startswith("sel_sub_"):
        await subject_selected_callback(update, context)
        return

    if data.startswith("sel_cnt_"):
        await country_selected_callback(update, context)
        return

    if data.startswith("sel_typ_"):
        await type_selected_callback(update, context)
        return

    if data.startswith("opp_page_"):
        await opp_page_callback(update, context)
        return

    # Waiting university filters
    if data.startswith("w_cnt_"):
        await waiting_country_selected_callback(update, context)
        return

    if data.startswith("w_page_"):
        await waiting_page_callback(update, context)
        return

    # Professor filters (Subject-wise ONLY)
    if data.startswith("p_sub_"):
        await prof_subject_selected_callback(update, context)
        return

    if data.startswith("p_page_"):
        await prof_page_callback(update, context)
        return

    await query.answer()

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if "Explore OpenSTEM" in text:
        await explore_openstem_handler(update, context)
    elif "Explore Your Opportunity" in text:
        await start_opportunity_flow(update, context)
    elif "Explore Your Waiting University" in text:
        await start_waiting_flow(update, context)
    elif "Explore Professor for Perfect Research" in text:
        await start_professors_flow(update, context)
    elif "How OpenSTEM Will Help You" in text:
        await how_openstem_helps_handler(update, context)
    elif "Free Courses & Test Preparation" in text or "course" in text.lower():
        await free_courses_handler(update, context)
    elif "Join in Partnership Programme" in text or "partner" in text.lower():
        await partnership_handler(update, context)
    else:
        await start_command(update, context)

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Error occurred while handling update: %s", context.error, exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ An issue occurred while loading this section. Please tap /start to refresh the menu.",
                parse_mode=ParseMode.HTML
            )
        except Exception:
            pass

async def run_bot_forever():
    logger.info("Initializing OpenSTEM Telegram Bot (@Openstem_bot)...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("explore", explore_openstem_handler))
    app.add_handler(CommandHandler("opportunities", start_opportunity_flow))
    app.add_handler(CommandHandler("universities", start_waiting_flow))
    app.add_handler(CommandHandler("professors", start_professors_flow))
    app.add_handler(CommandHandler("how_it_helps", how_openstem_helps_handler))
    app.add_handler(CommandHandler("courses", free_courses_handler))
    app.add_handler(CommandHandler("partnership", partnership_handler))

    # Text message handler (Main Menu Buttons)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    # All inline callbacks
    app.add_handler(CallbackQueryHandler(callback_router))

    # Global error handler
    app.add_error_handler(global_error_handler)

    # Start background HTTP server in a separate thread for cloud hosting
    t = threading.Thread(target=start_health_server, daemon=True)
    t.start()

    # Explicit async initialization and start
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    bot_info = await app.bot.get_me()
    logger.info("Bot is 100%% active and polling as @%s (ID: %s) with 7 buttons!", bot_info.username, bot_info.id)

    # Keep running indefinitely
    stop_signal = asyncio.Event()
    await stop_signal.wait()

def main():
    asyncio.run(run_bot_forever())

if __name__ == "__main__":
    main()
