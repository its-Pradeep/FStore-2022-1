import os
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .commands import start, BATCH
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()

    # help text
    help_text = """**You need Help! Read this 👇**

★ Just send me the files, I will store file and give you share able link.\n\n☆ **My Features**\n\n• Support Channels! 👇\n• Files Store Permanent!\n• Support any Telegram Media with any size.\n• Support Message (media) with URL Buttons .\n• Remove Forward Tag also.\n You Can Enable or Disable Uploader Details in Caption by /mode. 👇\n• You Can Store Multiple files in one link by /batch!\n• You can delete your file while saving files in private. 🤗\n• You will get your info by /me 🙃\n\n💥 **Your files is Totally Safe by a Unique Code!**✌\n\n**📍Remember**\n\n• Please Don't Send Adults files.\n• Don't spam!\n• If Bot Stop, Check 👉 Status on Home --> **Know More** Button.\n\n


**You can use me in channel too 😉**

★ Make me admin in your channel with edit permission. Thats enough now continue uploading files in channel, I will edit all posts and add share able link url buttons.

**How to Enable uploader details in caption!**

★ Use /mode command to change and also you can use `/mode channel_id` to control caption for channel msg.\n\n🚶‍♂️ Thank You!!"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('About 📕', callback_data='about')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    owner = await c.get_users(int(OWNER_ID))
    bot = await c.get_me()

    # about text
    about_text = f"""--**My Details :**--

🤖 **My Name** : {bot.mention(style='md')}
    
📝 **Language** : [Python 3](https://www.python.org/)

🧰 **Framework** : [Pyrogram](https://github.com/pyrogram/pyrogram)

👨‍💻 **Creator** : [This Person](https://t.me/HKrrish)

🤗 **Credit** : [@Anoymous_Ns](https://t.me/Anoymous_Ns)

👥 **Contact** : [Here](https://t.me/KrAsst_Bot)

🌐 **Help** :  [Click Here](https://telegra.ph/TG-File-Store-Bot-05-25-2)
"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Help 💡', callback_data='help')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing message
    await m.message.edit(
        text=about_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^home$'))
async def home_cb(c, m):
    await m.answer()
    await start(c, m, cb=True)


@Client.on_callback_query(filters.regex('^done$'))
async def done_cb(c, m):
    BATCH.remove(m.from_user.id)
    c.cancel_listener(m.from_user.id)
    await m.message.delete()


@Client.on_callback_query(filters.regex('^delete'))
async def delete_cb(c, m):
    await m.answer()
    cmd, msg_id = m.data.split("+")
    chat_id = m.from_user.id if not DB_CHANNEL_ID else int(DB_CHANNEL_ID)
    message = await c.get_messages(chat_id, int(msg_id))
    await message.delete()
    await m.message.edit("Deleted files successfully 👨‍✈️")
