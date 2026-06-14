import asyncio
from pyrogram import enums, errors, filters, types

from Elevenyts import app, config, db, lang
from Elevenyts.helpers import buttons, utils

# You can change this to any image URL (anime, Monkey D. Luffy, etc.)
CUSTOM_START_IMG = "https://files.catbox.moe/d580rf.jpeg"  # <-- CHANGE THIS URL

@app.on_message(filters.command(["help"]) & filters.private & ~app.bl_users)
@lang.language()
async def _help(_, m: types.Message):
    """Handle /help command in private chats - shows help menu with image."""
    try:
        await m.delete()
    except Exception:
        pass
    
    try:
        await m.reply_photo(
            photo=CUSTOM_START_IMG,  # Use same custom image for help
            caption=m.lang["help_menu"],
            reply_markup=buttons.help_markup(m.lang),
            quote=True,
        )
    except Exception:
        await m.reply_text(
            text=m.lang["help_menu"],
            reply_markup=buttons.help_markup(m.lang),
            quote=True,
        )

@app.on_message(filters.command(["start"]))
@lang.language()
async def start(_, message: types.Message):
    """
    Monkey D. Luffy Music Bot – Custom welcome with sticker animation.
    """
    # Auto-delete command message in group chats
    if message.chat.type != enums.ChatType.PRIVATE:
        try:
            await message.delete()
        except Exception:
            pass
    
    if not message.from_user:
        return

    if message.from_user.id in app.bl_users and message.from_user.id not in db.notified:
        return await message.reply_text(message.lang["bl_user_notify"])

    if len(message.command) > 1 and message.command[1] == "help":
        return await _help(_, message)

    private = message.chat.type == enums.ChatType.PRIVATE

    # 🔥 Custom welcome message for Monkey D. Luffy Bot
    if private:
        # Private chat message (includes user's first name)
        _text = (
            f"⚓ **Yo Ho Ho, {message.from_user.first_name}!** ⚓\n\n"
            f"🎵 I'm **Monkey D. Luffy**, your music-playing pirate captain!\n"
            f"🏴‍☠️ I'm here to play high-quality songs, manage playlists, and bring the party to your crew.\n\n"
            f"🎧 Just send me a song name or YouTube link in any group where I'm an admin.\n"
            f"📖 Use /help to see all my commands.\n\n"
            f"👉 **Click the buttons below to add me to your group or visit my channel!**"
        )
    else:
        # Group chat message (short welcome)
        _text = (
            f"🏴‍☠️ **Monkey D. Luffy** is here!\n"
            f"🎶 Send `/play <song name>` to start the music.\n"
            f"📖 Type /help for all commands."
        )

    key = buttons.start_key(message.lang, private)
    
    # 1️⃣ Send sticker first
    sticker_msg = await message.reply_sticker(
        "CAACAgIAAxkBAAERY5BqLmEBxz9fh5wcpacN1fIEpwdEtwACPUcAAisAAUFK1dzLvSrysQk8BA",
        quote=not private
    )
    
    # 2️⃣ Wait 6 seconds, then vanish
    await asyncio.sleep(6)
    try:
        await sticker_msg.delete()
    except Exception:
        pass  # Ignore deletion errors
    
    # 3️⃣ Send welcome photo with custom message
    try:
        await message.reply_photo(
            photo=CUSTOM_START_IMG,  # Use your new Luffy-themed image
            caption=_text,
            reply_markup=key,
            quote=not private,
        )
    except errors.ChatSendPhotosForbidden:
        # If photos are blocked, send text only
        await message.reply_text(
            text=_text,
            reply_markup=key,
            quote=not private,
        )

    # Add new users to database (private chats only)
    if private:
        if await db.is_user(message.from_user.id):
            return
        await utils.send_log(message)
        return await db.add_user(message.from_user.id)

@app.on_message(filters.command(["playmode", "settings"]) & filters.group & ~app.bl_users)
@lang.language()
async def settings(_, message: types.Message):
    """Group settings (unchanged)."""
    try:
        await message.delete()
    except Exception:
        pass
    
    admin_only = await db.get_play_mode(message.chat.id)
    _language = "en"
    await utils.safe_text(
        message,
        message.lang["start_settings"].format(message.chat.title),
        reply_markup=buttons.settings_markup(
            message.lang, admin_only, _language, message.chat.id
        ),
        quote=True,
    )

@app.on_message(filters.new_chat_members, group=7)
@lang.language()
async def _new_member(_, message: types.Message):
    """Leave non-supergroups, add new chats to DB (unchanged)."""
    if message.chat.type != enums.ChatType.SUPERGROUP:
        return await message.chat.leave()

    for member in message.new_chat_members:
        if member.id == app.id:
            if await db.is_chat(message.chat.id):
                return
            await db.add_chat(message.chat.id)
