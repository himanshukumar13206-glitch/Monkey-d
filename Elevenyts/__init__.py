# ==========================================================
# Copyright (c) 2026 ArtistBots
# All Rights Reserved.
#
# Project      : ArtistBots API Telegram Music Bot
# Powered By   : Artist
# Type         : API Based Telegram Music Bot
#
# Bot          : @ArtistApibot
# Channel      : https://t.me/artistbots
# GitHub       : https://github.com/elevenyts
#
# Unauthorized copying, modification, or redistribution
# of this source code without permission is prohibited.
# ==========================================================
import asyncio
import time
import logging
from logging.handlers import RotatingFileHandler
from typing import List
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Import your start module components
from Elevenyts.plugins.start import register_start_handlers, CallbackHandler

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create the bot client
app = Client(
    "MonkeyDLuffyBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Elevenyts/plugins")   # This loads all plugins automatically
)

# ========== ADD THE REGISTRATION CODE HERE ==========
def register_handlers():
    callback_handler = CallbackHandler()
    register_start_handlers(app, callback_handler)
    logging.info("Premium start menu handlers registered")

# Run this after client is created but before app.run()
register_handlers()
# ====================================================

if __name__ == "__main__":
    logging.info("Starting Monkey D Luffy Music Bot...")
    app.run()   # This starts the bot
# Configure logging
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

# Reduce noise from third-party libraries
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

logger = logging.getLogger("Elevenyts")

# Version
__version__ = "3.0.1"

# Load configuration
from config import Config

config = Config()
config.check()

# Global task list for background tasks
tasks: List = []
boot: float = time.time()

# Initialize bot client
from Elevenyts.core.bot import Bot
app = Bot()

# Ensure required directories exist
from Elevenyts.core.dir import ensure_dirs
ensure_dirs()

# Initialize userbot/assistant clients
from Elevenyts.core.userbot import Userbot
userbot = Userbot()

# Initialize database connection
from Elevenyts.core.mongo import MongoDB
db = MongoDB()

# Initialize language system
from Elevenyts.core.lang import Language
lang = Language()

# Initialize Telegram and YouTube utilities
from Elevenyts.core.telegram import Telegram
from Elevenyts.core.youtube import YouTube
tg = Telegram()
yt = YouTube()

# Initialize preload manager for background track downloading
from Elevenyts.core.preload import PreloadManager
preload = PreloadManager()

# Initialize queue manager
from Elevenyts.helpers import Queue
queue = Queue()

# Initialize preload manager for next-track downloading
from Elevenyts.helpers._preload import PreloadManager
preload = PreloadManager()

# Initialize call handler
from Elevenyts.core.calls import TgCall
tune = TgCall()


async def stop() -> None:
    """
    Gracefully shutdown the bot and all its components.
    
    This function:
    - Cancels all running background tasks
    - Closes bot and userbot connections
    - Closes database connection
    - Logs shutdown completion
    """
    logger.info("🛑 Stopping bot...")
    
    # Cancel all background tasks
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            # Expected when cancelling tasks - suppress the error
            pass
        except Exception:
            pass
    
    # Close all connections
    await app.exit()
    await userbot.exit()
    await db.close()
    
    logger.info("✅ Bot stopped successfully.\n")
