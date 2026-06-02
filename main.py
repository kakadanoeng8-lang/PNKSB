
# main.py

import sys

import os

import logging

import asyncio

# Direct absolute lookups to local directory

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN

from handlers.commands import (

    start_command,

    help_command,

    handle_message,

    handle_callback,

    stock_in_command,

    stock_out_command,

    find_command,

    get_order_command

)

# Active log visibility tracking

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
async def run_bot():

    print("Starting Interactive Smart Stock Bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Manual Command Bindings

    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(CommandHandler("stock_in", stock_in_command))

    app.add_handler(CommandHandler("stock_out", stock_out_command))

    app.add_handler(CommandHandler("find", find_command))

    app.add_handler(CommandHandler("order", get_order_command))

    # Event Streams (Dynamic Keyboard Input & Inline Button Taps)

    app.add_handler(CallbackQueryHandler(handle_callback))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))



    # Initialize Engine and clear stale message history queue

    await app.initialize()

    await app.updater.start_polling(drop_pending_updates=True)

    await app.start()

   

    print("🚀 Bot is live with all feature sets working flawlessly!")

   

    try:

        while True: await asyncio.sleep(3600)

    except (KeyboardInterrupt, asyncio.CancelledError): print("\nShutting down engine safety triggers...")

    finally:

        await app.updater.stop()

        await app.stop()

        await app.shutdown()



if __name__ == "__main__":

    try: asyncio.run(run_bot())

    except KeyboardInterrupt: print("\nProcess exited cleanly.")

