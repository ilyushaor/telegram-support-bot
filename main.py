{\rtf1\ansi\ansicpg1251\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import logging\
from aiogram import Bot, Dispatcher, types\
from aiogram.utils import executor\
\
logging.basicConfig(level=logging.INFO)\
\
API_TOKEN = os.getenv("BOT_TOKEN")\
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))\
\
bot = Bot(token=API_TOKEN)\
dp = Dispatcher(bot)\
\
users = set()\
\
@dp.message_handler(content_types=types.ContentType.ANY)\
async def handle_user_message(message: types.Message):\
    users.add(message.from_user.id)\
    user_info = f"\uc0\u55357 \u56460  \u1057 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077  \u1086 \u1090  @\{message.from_user.username or message.from_user.full_name\} (id: \{message.from_user.id\}):"\
    if message.text:\
        await bot.send_message(ADMIN_CHAT_ID, f"\{user_info\}\\n\{message.text\}")\
    elif message.photo:\
        await bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=user_info)\
    elif message.document:\
        await bot.send_document(ADMIN_CHAT_ID, message.document.file_id, caption=user_info)\
\
@dp.message_handler(lambda m: m.reply_to_message and "id:" in m.reply_to_message.text)\
async def reply_to_user(message: types.Message):\
    try:\
        user_id = int(message.reply_to_message.text.split("id:")[1].split(")")[0])\
        await bot.send_message(user_id, f"\uc0\u55357 \u56553  \u1054 \u1090 \u1074 \u1077 \u1090  \u1072 \u1076 \u1084 \u1080 \u1085 \u1080 \u1089 \u1090 \u1088 \u1072 \u1090 \u1086 \u1088 \u1072 :\\n\{message.text\}")\
        await message.answer("\uc0\u9989  \u1054 \u1090 \u1074 \u1077 \u1090  \u1086 \u1090 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1102 .")\
    except Exception as e:\
        await message.answer(f"\uc0\u9888 \u65039  \u1054 \u1096 \u1080 \u1073 \u1082 \u1072 : \{e\}")\
\
@dp.message_handler(lambda m: m.text and m.text.startswith("!\uc0\u1088 \u1072 \u1089 \u1089 \u1099 \u1083 \u1082 \u1072 "))\
async def broadcast(message: types.Message):\
    if message.chat.id != ADMIN_CHAT_ID:\
        return\
    text = message.text.replace("!\uc0\u1088 \u1072 \u1089 \u1089 \u1099 \u1083 \u1082 \u1072 ", "").strip()\
    sent = 0\
    for user_id in users:\
        try:\
            await bot.send_message(user_id, text)\
            sent += 1\
        except:\
            pass\
    await message.answer(f"\uc0\u9989  \u1056 \u1072 \u1089 \u1089 \u1099 \u1083 \u1082 \u1072  \u1086 \u1090 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 \u1072  \{sent\} \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103 \u1084 .")\
\
if __name__ == "__main__":\
    executor.start_polling(dp, skip_updates=True)\
}