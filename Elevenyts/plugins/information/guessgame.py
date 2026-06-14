from pyrogram import filters
from Elevenyts import app
import random

# Store active games (chat_id → number)
active_games = {}

@app.on_message(filters.command("guess") & filters.group)
async def guess_game(_, message):
    chat_id = message.chat.id
    if chat_id in active_games:
        await message.reply_text("🎲 A game is already in progress! Use /stopgame to end it.")
        return

    number = random.randint(1, 100)
    active_games[chat_id] = number
    await message.reply_text("🤔 I’ve picked a number between 1 and 100. Start guessing!")

@app.on_message(filters.group & ~filters.command("guess") & ~filters.command("stopgame"))
async def check_guess(_, message):
    chat_id = message.chat.id
    if chat_id not in active_games:
        return

    try:
        guess = int(message.text.strip())
    except ValueError:
        return

    target = active_games[chat_id]
    if guess == target:
        await message.reply_text(f"🎉 Correct! {message.from_user.first_name} wins! 🎉")
        del active_games[chat_id]
    elif guess < target:
        await message.reply_text("📉 Too low! Try a higher number.")
    else:
        await message.reply_text("📈 Too high! Try a lower number.")

@app.on_message(filters.command("stopgame") & filters.group)
async def stop_game(_, message):
    chat_id = message.chat.id
    if chat_id in active_games:
        del active_games[chat_id]
        await message.reply_text("🛑 Game stopped.")
    else:
        await message.reply_text("❌ No active game to stop.")
