import asyncio
from traceback import format_exc
from pyrogram.errors import RPCError

from Opus import app
from config import LOGGER_ID  

async def notify_logger_about_crash(error: Exception):
    error_text = (
        "🚨 <b><u>ʙᴏᴛ ᴄʀᴀꜱʜ ᴀʟᴇʀᴛ</u></b>\n\n"
        f"<b>ᴇʀʀᴏʀ:</b> <code>{str(error)}</code>\n\n"
        f"<b>ᴛʀᴀᴄᴇʙᴀᴄᴋ:</b>\n<pre>{format_exc()}</pre>"
    )
    try:
        await app.send_message(
            chat_id=LOGGER_ID,
            text=error_text,
            disable_web_page_preview=True
        )
    except RPCError:
        pass

def logger_alert_on_crash(func):
    async def wrapper(client, *args, **kwargs):
        try:
            return await func(client, *args, **kwargs)
        except Exception as e:
            await notify_logger_about_crash(e)
            raise 
    return wrapper

def setup_global_exception_handler():
    loop = asyncio.get_event_loop()

    def handle_exception(loop, context):
        error = context.get("exception")
        if error:
            asyncio.create_task(notify_logger_about_crash(error))

    loop.set_exception_handler(handle_exception)
