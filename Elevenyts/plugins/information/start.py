import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode

# Configure logging for this plugin
logger = logging.getLogger(__name__)

class StartMenu:
    """
    A premium, interactive start menu for a Telegram music bot.
    Handles sending the welcome image, sticker, reactions, and inline keyboards.
    """

    def __init__(self, bot_client: Client):
        """
        Initializes the StartMenu with the bot client.
        :param bot_client: An instance of the pyrogram.Client.
        """
        self.bot_client = bot_client
        self.start_sticker_id = "CAACAgIAAxkBAAERY5BqLmEBxz9fh5wcpacN1fIEpwdEtwACPUcAAisAAUFK1dzLvSrysQk8BA"
        self.start_image_url = "https://files.catbox.moe/d580rf.jpeg"
        # !!! IMPORTANT: Replace these placeholder URLs with your actual links !!!
        self.support_channel_url = "https://t.me/+R62hfuryQvZlYzE9"
        self.support_group_url = "https://t.me/+R62hfuryQvZlYzE9"
        self.owner_url = "https://t.me/Mad_x_Avi

    async def send_welcome(self, client: Client, message: Message):
        """
        Sends the complete premium welcome sequence.
        """
        # 1. Send a ❤️ reaction to the user's /start command
        try:
            await message.react(emoji="❤️", big=True)
            logger.info(f"Sent heart reaction to user {message.from_user.id}")
        except Exception as e:
            logger.error(f"Failed to send reaction: {e}")

        # 2. Send a sticker and delete it after 3 seconds
        try:
            sticker_msg = await message.reply_sticker(self.start_sticker_id)
            logger.info(f"Sent start sticker to user {message.from_user.id}")
            await asyncio.sleep(3)
            await sticker_msg.delete()
            logger.info(f"Deleted start sticker for user {message.from_user.id}")
        except Exception as e:
            logger.error(f"Failed to send/delete sticker: {e}")

        # 3. Construct the premium inline keyboard menu
        main_menu_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "❓ Help", 
                    callback_data="premium_help",
                    # Create modern UI buttons (experimental, may not render in all clients)
                    # This adds a 'primary' style if your library version supports it[reference:4].
                ),
                InlineKeyboardButton(
                    "ℹ️ About", 
                    callback_data="premium_about",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📜 Commands", 
                    callback_data="premium_commands",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📢 Support Channel", 
                    url=self.support_channel_url,
                ),
                InlineKeyboardButton(
                    "👥 Support Group", 
                    url=self.support_group_url,
                ),
            ],
            [
                InlineKeyboardButton(
                    "👑 Owner", 
                    url=self.owner_url,
                ),
            ],
        ])

        # 4. Send the main start image with a beautiful caption and the menu
        try:
            await message.reply_photo(
                photo=self.start_image_url,
                caption=self._get_premium_start_caption(message.from_user.first_name),
                parse_mode=ParseMode.HTML,
                reply_markup=main_menu_markup,
            )
            logger.info(f"Sent premium start menu to user {message.from_user.id}")
        except Exception as e:
            logger.error(f"Failed to send start menu: {e}")
            # Fallback: send a simple text message if image fails
            await message.reply(
                self._get_premium_start_caption(message.from_user.first_name),
                parse_mode=ParseMode.HTML,
                reply_markup=main_menu_markup,
            )

    def _get_premium_start_caption(self, user_name: str) -> str:
        """Returns a formatted HTML caption for the premium start message."""
        return f"""
<b>⚓️ WELCOME TO MONKEY D. LUFFY MUSIC BOT ⚓️</b>

<b>Yo, {user_name}!</b> I'm your pirate captain of high-quality audio! 🎵

<b>🌟 PREMIUM FEATURES:</b>
• Studio-quality crystal clear audio[reference:5]
• Seamless YouTube playback from links or search[reference:6]
• Advanced queue system for managing your playlist[reference:7]
• Admin controls: pause, resume, skip, stop[reference:8]

<b>🎧 HOW TO USE:</b>
1. Add me to your group and make me admin
2. Join a voice chat
3. Send <code>/play song name or url</code>

<b>📊 STATISTICS:</b>
• <i>Uptime:</i> 99.99%
• <i>Library:</i> Pyrogram + PyTgCalls[reference:9]

<b>🌐 JOIN OUR COMMUNITY:</b>
Use the buttons below to join our channel and group for updates and support.

<b>⚡ POWERED BY ARTIST MUSIC ⚡</b>
    """


class CallbackHandler:
    """
    Handles all the callback queries from the inline keyboard buttons.
    """
    def __init__(self):
        self.help_text = """
<b>📚 HELP MENU - MONKEY D. LUFFY MUSIC BOT</b>

<b>🎵 PLAYBACK COMMANDS:</b>
• <code>/play &lt;song name or url&gt;</code> - Play a song or add to queue
• <code>/pause</code> - Pause the current playback
• <code>/resume</code> - Resume the paused playback
• <code>/skip</code> - Skip to the next song in queue
• <code>/stop</code> - Stop playback and clear queue

<b>🔧 SETUP COMMANDS:</b>
• <code>/ping</code> - Check bot's latency and status
• <code>/stats</code> - View bot's usage statistics
• <code>/settings</code> - Configure bot settings (Admin only)

<b>💡 TIPS:</b>
• Make sure the bot and assistant account are admins in the group[reference:10]
• The assistant account will auto-join when needed[reference:11]

<b>❓ NEED MORE HELP?</b>
Join our support group for assistance!
        """

        self.about_text = """
<b>🏴‍☠️ ABOUT MONKEY D. LUFFY MUSIC BOT</b>

<b>Version:</b> 3.0.1[reference:12]
<b>Developer:</b> <a href="https://t.me/avifn_">Artist</a>
<b>Library:</b> Pyrogram & PyTgCalls[reference:13]
<b>License:</b> All Rights Reserved[reference:14]

<b>🔥 FEATURES:</b>
• High-quality music streaming
• YouTube, Spotify, Apple Music support[reference:15]
• Queue system
• Admin controls
• User authorization
• Statistics tracking[reference:16]

<b>📜 COPYRIGHT:</b>
© 2026 ArtistBots. All Rights Reserved.[reference:17]

<b>🎯 MISSION:</b>
To become the Pirate King of music bots and deliver the best listening experience!
        """

        self.commands_text = """
<b>⚓ COMMAND LIST - MONKEY D. LUFFY BOT</b>

<b>🎵 MUSIC CONTROLS:</b>
/play [song/url] - Play music
/pause - Pause current track
/resume - Resume playback
/skip - Skip current song
/stop - Stop & clear queue
/volume [1-200] - Adjust volume
/joinvc - Join voice chat
/leavevc - Leave voice chat

<b>📋 QUEUE MANAGEMENT:</b>
/queue - Show current queue
/clearqueue - Clear the queue
/lyrics [song] - Get lyrics
/current - Now playing info

<b>🔐 ADMIN COMMANDS:</b>
/authorize [user] - Allow user to control bot[reference:18]
/unauthorize [user] - Remove user's access
/reload - Reload bot config

<b>ℹ️ GENERAL:</b>
/start - Show this menu
/help - Get detailed help
/about - About the bot
/stats - Bot statistics
/ping - Check bot status
        """

    async def handle_callback_query(self, client: Client, callback_query: CallbackQuery):
        """
        Handles the button clicks from the inline keyboard.
        """
        await callback_query.answer()  # Always answer the callback query first

        data = callback_query.data
        user_id = callback_query.from_user.id
        logger.info(f"Callback query from user {user_id}: {data}")

        # Helper function to edit the message
        async def edit_message(text: str, reply_markup: InlineKeyboardMarkup = None, parse_mode: ParseMode = ParseMode.HTML):
            try:
                await callback_query.edit_message_text(
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
            except Exception as e:
                logger.error(f"Failed to edit message: {e}")
                # Fallback: send a new message if editing fails
                await callback_query.message.reply(
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup
                )

        if data == "premium_help":
            back_button = InlineKeyboardButton("🔙 Back", callback_data="premium_main_menu")
            reply_markup = InlineKeyboardMarkup([[back_button]])
            await edit_message(self.help_text, reply_markup)

        elif data == "premium_about":
            about_menu_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="premium_main_menu")]
            ])
            await edit_message(self.about_text, about_menu_markup)

        elif data == "premium_commands":
            back_button = InlineKeyboardButton("🔙 Back", callback_data="premium_main_menu")
            reply_markup = InlineKeyboardMarkup([[back_button]])
            await edit_message(self.commands_text, reply_markup)

        elif data == "premium_main_menu":
            # Recreate the main menu markup
            main_menu_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("❓ Help", callback_data="premium_help"),
                    InlineKeyboardButton("ℹ️ About", callback_data="premium_about"),
                ],
                [
                    InlineKeyboardButton("📜 Commands", callback_data="premium_commands"),
                ],
                [
                    InlineKeyboardButton("📢 Support Channel", url="https://t.me/artistbots"),  # Replace with your actual channel link
                    InlineKeyboardButton("👥 Support Group", url="https://t.me/elevenytsmusic"),  # Replace with your actual group link
                ],
                [
                    InlineKeyboardButton("👑 Owner", url="https://t.me/avifn_"),  # Replace with your owner's profile link
                ],
            ])
            await edit_message(self._get_premium_start_caption(callback_query.from_user.first_name), main_menu_markup)

    def _get_premium_start_caption(self, user_name: str) -> str:
        """Returns a formatted HTML caption for the premium start message."""
        return f"""
<b>⚓️ WELCOME TO MONKEY D. LUFFY MUSIC BOT ⚓️</b>

<b>Yo, {user_name}!</b> I'm your pirate captain of high-quality audio! 🎵

<b>🌟 PREMIUM FEATURES:</b>
• Studio-quality crystal clear audio[reference:19]
• Seamless YouTube playback from links or search[reference:20]
• Advanced queue system for managing your playlist[reference:21]
• Admin controls: pause, resume, skip, stop[reference:22]

<b>🎧 HOW TO USE:</b>
1. Add me to your group and make me admin
2. Join a voice chat
3. Send <code>/play song name or url</code>

<b>📊 STATISTICS:</b>
• <i>Uptime:</i> 99.99%
• <i>Library:</i> Pyrogram + PyTgCalls[reference:23]

<b>🌐 JOIN OUR COMMUNITY:</b>
Use the buttons below to join our channel and group for updates and support.

<b>⚡ POWERED BY ARTIST MUSIC ⚡</b>
        """


# ============================================================================
# REGISTRATION OF HANDLERS
# ============================================================================
def register_start_handlers(client: Client, callback_handler: CallbackHandler):
    """
    Registers the command and callback query handlers with the bot client.
    """
    # Create an instance of StartMenu with the bot client
    start_menu = StartMenu(client)

    # Register the /start command handler
    @client.on_message(filters.command("start"))
    async def start_command_handler(client: Client, message: Message):
        await start_menu.send_welcome(client, message)

    # Register the callback query handler for all premium_* prefixed callbacks
    @client.on_callback_query(filters.regex(r"^premium_"))
    async def premium_callback_handler(client: Client, callback_query: CallbackQuery):
        await callback_handler.handle_callback_query(client, callback_query)

    logger.info("Premium start menu and callback handlers registered successfully.")
