import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = set()

@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_user_message(message: types.Message):
    users.add(message.from_user.id)
    user_info = f"💌 Сообщение от @{message.from_user.username or message.from_user.full_name} (id: {message.from_user.id}):"
    if message.text:
        await bot.send_message(ADMIN_CHAT_ID, f"{user_info}\n{message.text}")
    elif message.photo:
        await bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=user_info)
    elif message.document:
        await bot.send_document(ADMIN_CHAT_ID, message.document.file_id, caption=user_info)

@dp.message_handler(lambda m: m.reply_to_message and "id:" in m.reply_to_message.text)
async def reply_to_user(message: types.Message):
    try:
        user_id = int(message.reply_to_message.text.split("id:")[1].split(")")[0])
        await bot.send_message(user_id, f"📩 Ответ администратора:\n{message.text}")
        await message.answer("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")

@dp.message_handler(lambda m: m.text and m.text.startswith("!рассылка"))
async def broadcast(message: types.Message):
    if message.chat.id != ADMIN_CHAT_ID:
        return
    text = message.text.replace("!рассылка", "").strip()
    sent = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            sent += 1
        except:
            pass
    await message.answer(f"✅ Рассылка отправлена {sent} пользователям.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

