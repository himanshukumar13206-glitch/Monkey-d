# ... (everything above remains unchanged) ...
import asyncio
from pyrogram import enums, errors, filters, types

from Elevenyts import app, config, db, lang
from Elevenyts.helpers import buttons, utils
@app.on_message(filters.command(["start"]))
@lang.language()
async def start(_, message: types.Message):
    """
    Handle /start command - welcome message for users.

    - In private chat: Shows welcome message with inline buttons
    - In group chat: Shows short welcome message
    - Adds new users to database
    - Sends log to logger group for new users
    - Sends a sticker that vanishes after 6 seconds, then shows photo
    """
    # Auto-delete command message in group chats
    if message.chat.type != enums.ChatType.PRIVATE:
        try:
            await message.delete()
        except Exception:
            pass
    
    # Skip if message from channel or anonymous admin
    if not message.from_user:
        return

    # Check if user is blacklisted
    if message.from_user.id in app.bl_users and message.from_user.id not in db.notified:
        return await message.reply_text(message.lang["bl_user_notify"])

    # If /start help, show help menu
    if len(message.command) > 1 and message.command[1] == "help":
        return await _help(_, message)

    # Determine if chat is private or group
    private = message.chat.type == enums.ChatType.PRIVATE

    # Choose appropriate welcome message
    _text = (
        message.lang["start_pm"].format(message.from_user.first_name, app.name)
        if private
        else message.lang["start_gp"].format(app.name)
    )

    key = buttons.start_key(message.lang, private)
    
    # 1️⃣ Send sticker first (with your provided ID)
    sticker_msg = await message.reply_sticker(
        "CAACAgIAAxkBAAERY5BqLmEBxz9fh5wcpacN1fIEpwdEtwACPUcAAisAAUFK1dzLvSrysQk8BA",
        quote=not private
    )
    
    # 2️⃣ Wait 6 seconds
    await asyncio.sleep(6)
    
    # 3️⃣ Try to delete the sticker (vanish)
    try:
        await sticker_msg.delete()
    except Exception:
        pass  # Ignore if deletion fails (e.g., no permissions)
    
    # 4️⃣ Send welcome photo (or text fallback)
    try:
        await message.reply_photo(
            photo=config.START_IMG,
            caption=_text,
            reply_markup=key,
            quote=not private,
        )
    except errors.ChatSendPhotosForbidden:
        # If photos are not allowed, send text only
        await message.reply_text(
            text=_text,
            reply_markup=key,
            quote=not private,
        )

    # For private chats, add user to database if new
    if private:
        if await db.is_user(message.from_user.id):
            return  # User already exists, no need to add
        # Log new user to logger group
        await utils.send_log(message)
        # Add user to database
        return await db.add_user(message.from_user.id)

# ... (rest of the file unchanged) ...
