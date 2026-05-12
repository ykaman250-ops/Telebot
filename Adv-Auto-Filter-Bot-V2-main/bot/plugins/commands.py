#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation, LOGGER # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error

db = Database()

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    
    from bot.utils import get_shortlink, get_hash
    import time
    
    payload = update.command[1] if len(update.command) > 1 else None
    
    if payload:
        if payload.startswith("get_"):
            unique_id = payload.split("_")[1]
            timestamp = int(time.time())
            verify_hash = get_hash(update.from_user.id, unique_id, timestamp)
            
            bot_me = await bot.get_me()
            verify_url = f"https://t.me/{bot_me.username}?start=verify_{unique_id}_{timestamp}_{verify_hash}"
            
            wait_msg = await update.reply_text("🔗 Generating secure link...")
            short_url = await get_shortlink(verify_url)
            
            text = (
                "**🔒 File Locked**\n\n"
                "To unlock the file you requested, please watch a quick ad to verify you are a human.\n\n"
                "1. Click the button below.\n"
                "2. Complete the shortlink steps.\n"
                "3. You will be redirected back here for your file."
            )
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔓 Unlock File Now", url=short_url)]
            ])
            await wait_msg.edit_text(text, reply_markup=markup)
            return

        elif payload.startswith("verify_"):
            parts = payload.split("_")
            if len(parts) == 4:
                _, unique_id, timestamp, incoming_hash = parts
                
                expected_hash = get_hash(update.from_user.id, unique_id, timestamp)
                if incoming_hash != expected_hash:
                    await update.reply_text("❌ Invalid or corrupted verification link.")
                    return
                
                if int(time.time()) - int(timestamp) > 86400: # 24 hours
                    await update.reply_text("⏳ This verification link has expired. Please search and request the file again.")
                    return
                
                file_id, file_name, file_caption, file_type = await db.get_file(unique_id)
                if not file_id:
                    await update.reply_text("⚠️ File missing from database!")
                    return
                
                caption = file_caption if file_caption else (f"<code>{file_name}</code>")
                try:
                    await update.reply_cached_media(
                        file_id,
                        quote=True,
                        caption=caption,
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception as e:
                    await update.reply_text(f"<b>Error sending file:</b>\n<code>{e}</code>", quote=True, parse_mode=enums.ParseMode.HTML)
                    LOGGER(__name__).error(e)
                return

    buttons = [[
        InlineKeyboardButton('Developers', url='https://t.me/CrazyBotsz'),
        InlineKeyboardButton('Source Code 🧾', url ='https://github.com/CrazyBotsz/Adv-Auto-Filter-Bot-V2')
    ],[
        InlineKeyboardButton('Support 🛠', url='https://t.me/CrazyBotszGrp')
    ],[
        InlineKeyboardButton('Help ⚙', callback_data="help")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(
                update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('About 🚩', callback_data='about')
    ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )
