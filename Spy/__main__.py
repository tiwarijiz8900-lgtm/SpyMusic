import asyncio
import importlib
from threading import Thread
from flask import Flask
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Spy import LOGGER, app, userbot
from Spy.core.call import Sagar
from Spy.misc import sudo
from Spy.plugins import ALL_MODULES
from Spy.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# --- FLASK SERVER FOR 24/7 KEEP-ALIVE ---
web_app = Flask('')

@web_app.route('/')
def home():
    return "Spy Music Bot is Running 24/7!"

def run():
    # Render default port 8000 use karta hai
    web_app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
# ----------------------------------------

async def init():
    # Keep alive server start karein
    LOGGER("Spy").info("Starting Keep-Alive Web Server...")
    keep_alive()

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    
    await app.start()
    
    for all_module in ALL_MODULES:
        importlib.import_module("Spy.plugins" + all_module)
    
    LOGGER("Spy.plugins").info("sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ᴀʟʟ ᴍᴏᴅᴜʟᴇs...")
    
    await userbot.start()
    await Sagar.start()
    
    try:
        await Sagar.stream_call("https://te.legra.ph/file/39b302c93da5c457a87e3.mp4")
    except NoActiveGroupCall:
        LOGGER("Spy").error(
            "ʙsᴅᴋ ᴠᴄ ᴛᴏ ᴏɴ ᴋᴀʀʟᴇ  ʟᴏɢ ɢʀᴏᴜᴘ\ᴄʜᴀɴɴᴇʟ ᴋɪ.\n\n ᴏɴ ᴋᴀʀᴋᴇ ᴀᴀ ᴛᴀʙ ᴛᴀᴋ ʙᴏᴛ ʙᴀɴᴅ ᴋᴀʀ ʀʜᴀ ʜᴏᴏɴ..."
        )
        exit()
    except Exception as e:
        LOGGER("Spy").error(f"Stream Error: {e}")
        pass
        
    await Sagar.decorators()
    LOGGER("Spy").info(
        "ᴍᴜsɪᴄ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ, ɴᴏᴡ ɢɪʙ ʏᴏᴜʀ ɢɪʀʟғʀɪᴇɴᴅ ᴄʜᴜᴛ ɪɴ @LOVE_FEELINGS_WILL1"
    )
    
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("Spy").info("ᴍᴀᴀ ᴄʜᴜᴅᴀ ᴍᴀɪɴ ʙᴏᴛ ʙᴀɴᴅ ᴋᴀʀ ʀʜᴀ Sᴘʏ Mᴜsɪᴄ Bᴏᴛ...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
