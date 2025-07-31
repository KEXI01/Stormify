from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors import SlowmodeWait

from Opus import app
from Opus.misc import SUDOERS, db
from Opus.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
    is_skipmode,
)
from config import SUPPORT_CHAT, adminlist, confirmer
from strings import get_string

from ..formatters import int_to_alpha
import asyncio


# Helper to safely reply with slowmode and write error handling
async def safe_reply(message, text, **kwargs):
    try:
        return await message.reply_text(text, **kwargs)
    except SlowmodeWait as e:
        await asyncio.sleep(e.x)
        return await message.reply_text(text, **kwargs)
    except ChatWriteForbidden:
        return


# Helper to safely answer CallbackQuery
async def safe_answer(cb, text, **kwargs):
    try:
        return await cb.answer(text, **kwargs)
    except ChatWriteForbidden:
        return
    except SlowmodeWait as e:
        await asyncio.sleep(e.x)
        return await cb.answer(text, **kwargs)


def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        if not await is_maintenance():
            if message.from_user.id not in SUDOERS:
                return await safe_reply(
                    message,
                    f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]]
            )
            return await safe_reply(message, _["general_3"], reply_markup=upl)

        chat_id = message.chat.id
        if message.command and message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await safe_reply(message, _["setting_7"])
            try:
                await app.get_chat(chat_id)
            except:
                return await safe_reply(message, _["cplay_4"])

        if not await is_active_chat(chat_id):
            return await safe_reply(message, _["general_5"])

        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await safe_reply(message, _["admin_13"])
            if message.from_user.id not in admins:
                if await is_skipmode(message.chat.id):
                    upvote = await get_upvote_count(chat_id)
                    command = message.command[0]
                    MODE = command[1:] if command[0] == "c" else command
                    text = f"""<b>ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɴᴇᴇᴅᴇᴅ</b>

ʀᴇғʀᴇsʜ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ ᴠɪᴀ : /reload

» {upvote} ᴠᴏᴛᴇs ɴᴇᴇᴅᴇᴅ ғᴏʀ ᴘᴇʀғᴏʀᴍɪɴɢ ᴛʜɪs ᴀᴄᴛɪᴏɴ."""

                    if MODE == "speed":
                        return await safe_reply(message, _["admin_14"])

                    upl = InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton(
                                text="ᴠᴏᴛᴇ", callback_data=f"ADMIN UpVote|{chat_id}_{MODE.title()}"
                            )
                        ]]
                    )

                    try:
                        vidid = db[chat_id][0]["vidid"]
                        file = db[chat_id][0]["file"]
                    except:
                        return await safe_reply(message, _["admin_14"])

                    senn = await safe_reply(message, text, reply_markup=upl)
                    if chat_id not in confirmer:
                        confirmer[chat_id] = {}
                    confirmer[chat_id][senn.id] = {"vidid": vidid, "file": file}
                    return
                else:
                    return await safe_reply(message, _["admin_14"])

        return await mystic(client, message, _, chat_id)

    return wrapper


def AdminActual(mystic):
    async def wrapper(client, message):
        if not await is_maintenance():
            if message.from_user.id not in SUDOERS:
                return await safe_reply(
                    message,
                    f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]]
            )
            return await safe_reply(message, _["general_3"], reply_markup=upl)

        if message.from_user.id not in SUDOERS:
            try:
                member = await app.get_chat_member(message.chat.id, message.from_user.id)
                privs = member.privileges
                if not privs or not privs.can_manage_video_chats:
                    return await safe_reply(message, _["general_4"])
            except:
                return

        return await mystic(client, message, _)

    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if not await is_maintenance():
            if CallbackQuery.from_user.id not in SUDOERS:
                return await safe_answer(
                    CallbackQuery,
                    f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    show_alert=True,
                )

        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery, _)

        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                member = await app.get_chat_member(
                    CallbackQuery.message.chat.id, CallbackQuery.from_user.id
                )
                privs = member.privileges
                if not privs or not privs.can_manage_video_chats:
                    if CallbackQuery.from_user.id not in SUDOERS:
                        token = await int_to_alpha(CallbackQuery.from_user.id)
                        _check = await get_authuser_names(CallbackQuery.from_user.id)
                        if token not in _check:
                            return await safe_answer(
                                CallbackQuery, _["general_4"], show_alert=True
                            )
            except:
                return await safe_answer(CallbackQuery, _["general_4"], show_alert=True)

        return await mystic(client, CallbackQuery, _)

    return wrapper
