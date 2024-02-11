
import os
import re
import sys
import time
import datetime
import random 
import asyncio

from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType

from apscheduler.schedulers.background import BackgroundScheduler


API_ID = 90000
API_HASH = "Abcdefg1234hijklmnopqrstuvwxyz"
BOT_TOKEN = "1234567:AbCsFakkskkkksXyZ"
DEVS = [6048907378, 6190668142]

ALL_GROUPS = []
TOTAL_USERS = []
MEDIA_GROUPS = []
DISABLE_CHATS = []
GROUP_MEDIAS = {}

DELETE_MESSAGE = [
"1 Hour complete, I'm doing my work...🤞🏻",
"Its time to delete all medias!",
"No one can Copyright until I'm alive 馃槫",
"Hue hue, let's delete media...",
"I'm here to delete medias 馃檵", 
"馃槷鈥嶐煉� Finally I delete medias",
"Great work done by me 馃ゲ",
"All media cleared!😈",
"hue hue medias deleted by me 馃槷鈥嶐煉�",
"medias....",
"it's hard to delete all medias 馃檮",
]

START_MESSAGE = """
**Hello {}, I'm Anti - CopyRight Bot made by @The_Eternity_Soul Join me at @About_Zain**

 > **I can save your groups from Copyrights 馃槈**

 **Work:** I'll Delete all medias of your group in every 1 hour 鉃�
 
 **Process?:** Simply add me in your group and promote as admin with delete messages right!
"""

BUTTON = [[InlineKeyboardButton("+ Add me in group +", url="http://t.me/AntiCopyRightRobot?startgroup=s&admin=delete_messages")]]

Zain = Client('Anti-CopyRight-Bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def add_user(user_id):
   if user_id not in TOTAL_USERS:
      TOTAL_USERS.append(user_id)

@Zain.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
   start = datetime.datetime.now()
   add_user(e.from_user.id)
   rep = await e.reply_text("**Pong !!**")
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await rep.edit_text(f"馃 **PONG**: `{ms}`岽峴")

@Zain.on_message(filters.command(["help", "start"]))
async def start_message(_, message: Message):
   add_user(message.from_user.id)
   await message.reply(START_MESSAGE.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(BUTTON))

@Zain.on_message(filters.user(DEVS) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
   await e.reply("**Restarting.....**")
   try:
      await Zain.stop()
   except Exception:
      pass
   args = [sys.executable, "copyright.py"]
   os.execl(sys.executable, *args)
   quit()

@Zain.on_message(filters.user(DEVS) & filters.command(["stat", "stats"]))
async def status(_, message: Message):
   wait = await message.reply("Fetching.....")
   stats = "**Here is total stats of me!** \n\n"
   stats += f"Total Chats: `{len(ALL_GROUPS)}` \n"
   stats += f"Total users: `{len(TOTAL_USERS)}` \n"
   stats += f"Disabled chats: `{len(DISABLE_CHATS)}` \n"
   stats += f"Total Media active chats: `{len(MEDIA_GROUPS)}` \n\n"
   #stats += f"**漏 @The_Eternity_Soul**"
   await wait.edit_text(stats)


   
@Zain.on_message(filters.command(["anticopyright", "copyright"]))
async def enable_disable(Zain: Zain, message: Message):
   chat = message.chat
   if chat.id == message.from_user.id:
      await message.reply("Use this command in group!")
      return
   txt = ' '.join(message.command[1:])
   if txt:
      member = await Zain.get_chat_member(chat.id, message.from_user.id)
      if re.search("on|yes|enable".lower(), txt.lower()):
         if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply(f"Enabled anti-copyright! for {chat.title}")
               DISABLE_CHATS.remove(chat.id)
               return
            await message.reply("Already enabled!")

      elif re.search("no|off|disable".lower(), txt.lower()):
         if member.status == ChatMemberStatus.OWNER or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply("Already disabled!")
               return
            DISABLE_CHATS.append(chat.id)
            if chat.id in MEDIA_GROUPS:
               MEDIA_GROUPS.remove(chat.id)
            await message.reply(f"Disable Anti-CopyRight for {chat.title}!")
         else:
            await message.reply("Only chat Owner can disable anti-copyright!")
            return 
      else:
         if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply("Anti-Copyright is disable for this chat! \n\ntype `/anticopyright enable` to enable Anti-CopyRight")
            else:
               await message.reply("Anti-Copyright is enable for this chat! \n\ntype `/anticopyright disable` to disable Anti-CopyRight")
              
   else:
       if chat.id in DISABLE_CHATS:
          await message.reply("Anti-Copyright is disable for this chat! \n\ntype `/anticopyright enable` to enable Anti-CopyRight")
       else:
          await message.reply("Anti-Copyright is enable for this chat! \n\ntype `/anticopyright disable` to disable Anti-CopyRight")

@Zain.on_message(filters.all & filters.group)
async def watcher(_, message: Message):
   chat = message.chat
   user_id = message.from_user.id
   if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
      

      if chat.id not in ALL_GROUPS:
         ALL_GROUPS.append(chat.id)
      if chat.id in DISABLE_CHATS:
         return
      if chat.id not in MEDIA_GROUPS:
         if chat.id in DISABLE_CHATS:
            return
         MEDIA_GROUPS.append(chat.id)
      if (message.video or message.photo or message.animation or message.document):
         check = GROUP_MEDIAS.get(chat.id)
         if check:
            GROUP_MEDIAS[chat.id].append(message.id)
            print(f"Chat: {chat.title}, message ID: {message.id}")
         else:
            GROUP_MEDIAS[chat.id] = [message.id]
            print(f"Chat: {chat.title}, message ID: {message.id}")

def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
       return

    for i in MEDIA_GROUPS:
       addchat(i)
       if i in DISABLE_CHATS:
         return
       message_list = list(GROUP_MEDIAS.get(i))
       try:
          hue = Zain.send_message(i, random.choice(DELETE_MESSAGE))
          Zain.delete_messages(i, message_list, revoke=True)
          asyncio.sleep(1)
          hue.delete()
          GROUP_MEDIAS[i].delete()
       except Exception:
          pass
    MEDIA_GROUPS.remove(i)
    print("clean all medias 鉁�")
    print("waiting for 1 hour")

scheduler = BackgroundScheduler()
scheduler.add_job(AutoDelete, "interval", seconds=3600)

scheduler.start()

def starter():
   print('starting bot...')
   Zain.start()
   print('bot Started 鉁�')
   idle()

if __name__ == "__main__":
   starter()
