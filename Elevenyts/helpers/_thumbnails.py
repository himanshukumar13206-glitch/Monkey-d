import asyncio
from pyrogram import enums, errors, filters, types

from Elevenyts import app, config, db, lang
from Elevenyts.helpers import buttons, utils

# Your custom welcome image (change URL if needed)
CUSTOM_START_IMG = "https://graph.org/file/your_new_welcome_image.jpg"

@app.on_message(filters.command(["help"]) & filters.private & ~app.bl_users)
@lang.language()
async def _help(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass
    try:
        await m.reply_photo(
            photo=CUSTOM_START_IMG,
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
    # Auto-delete command in groups
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

    # ---------- YOUR EXACT WELCOME MESSAGE ----------
    if private:
        _text = (
            "✦ ʜєʏ Avi, ⊚ ᴛʜɪꜱ ɪꜱ Monkey D Luffy!\n\n"
            "✨ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴅᴇꜱɪɢɴᴇᴅ ᴍᴜꜱɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ꜰᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ & ᴄʜᴀɴɴᴇʟ.\n"
            "💖 ɪɴꜱᴛᴀɴᴛ ᴘʟᴀʏʙᴀᴄᴋ ᴡɪᴛʜᴏᴜᴛ ᴅᴇʟᴀʏꜱ\n\n"
            "⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ♡ **Avi**\n\n"
            "ɪꜰ ᴀɴʏ ʜᴇʟᴘ ᴛᴀᴘ ᴛᴏ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ.\n"
            "•── ⋅ ⋅ ────── ⋅᯽⋅ ────── ⋅ ⋅ ⋅──•"
        )
    else:
        _text = (
            "🏴‍☠️ **Monkey D. Luffy** is here!\n"
            "🎶 Send `/play <song name>` to start the music.\n"
            "📖 Type /help for all commands."
        )

    key = buttons.start_key(message.lang, private)

    # 1️⃣ Send sticker
    sticker_msg = await message.reply_sticker(
        "CAACAgIAAxkBAAERY5BqLmEBxz9fh5wcpacN1fIEpwdEtwACPUcAAisAAUFK1dzLvSrysQk8BA",
        quote=not private
    )
    await asyncio.sleep(6)
    try:
        await sticker_msg.delete()
    except Exception:
        pass

    # 2️⃣ Send welcome photo
    try:
        await message.reply_photo(
            photo=CUSTOM_START_IMG,
            caption=_text,
            reply_markup=key,
            quote=not private,
        )
    except errors.ChatSendPhotosForbidden:
        await message.reply_text(
            text=_text,
            reply_markup=key,
            quote=not private,
        )

    # Add user to DB
    if private:
        if await db.is_user(message.from_user.id):
            return
        await utils.send_log(message)
        return await db.add_user(message.from_user.id)

# ... (rest of your original functions like settings, _new_member remain unchanged)
