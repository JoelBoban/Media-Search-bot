import os
import logging
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from utils import Media, get_file_details, get_size
from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sᴏʀʀʏ Sɪʀ, Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ Tᴏ Usᴇ Mᴇ🤣.",
                        parse_mode="markdown",
                        
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="**Please Join My Updates Channel to use this Bot!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("👥 Jᴏɪɴ Mʏ Gʀᴏᴜᴘ", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🔄 Tʀʏ Aɢᴀɪɴ", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('🔁 Search again', switch_inline_query_current_chat=''),
                        InlineKeyboardButton('Mʏ Dᴇᴠ👨‍💻', url='https://t.me/stephennedumpally')
                    ]
                    ]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👥 Jᴏɪɴ Mʏ Gʀᴏᴜᴘ", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    else:
        await cmd.reply_photo(
            photo=(random.choice(["https://telegra.ph/file/6702ca45f631f6b229d41.jpg", "https://telegra.ph/file/89e4e72112da922830ffc.jpg", "https://telegra.ph/file/e7f1f33959540648ab417.jpg", "https://telegra.ph/file/b3aa3c0b2a316a64885b4.jpg", "https://telegra.ph/file/5002074da841f94952571.jpg"])),
            caption=START_MSG.format(cmd.from_user.mention),
            parse_mode="Markdown",
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Search Here 🔎", switch_inline_query_current_chat=''),
                        InlineKeyboardButton("Our Group 👥", url="https://t.me/askmecinema")
                    ],
                    [
                        InlineKeyboardButton("About 😎", callback_data="about")
                    ]
                ]
            )
        )


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Pʀᴏᴄᴇssɪɴɢ...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Sᴀᴠᴇᴅ Fɪʟᴇs: {total}')
    except Exception as e:
        logger.exception('Fᴀɪʟᴇᴅ Tᴏ Cʜᴇᴄᴋ Sᴀᴠᴇᴅ Fɪʟᴇs')
        await msg.edit(f'Eʀʀᴏʀ: {e}')


@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Pʀᴏᴄᴇssɪɴɢ...⏳", quote=True)
    else:
        await message.reply('Rᴇᴘʟʏ Tᴏ Fɪʟᴇ Wɪᴛʜ /delete Wʜɪᴄʜ Yᴏᴜ Wᴀɴᴛ Tᴏ Dᴇʟᴇᴛᴇ', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('Tʜɪs Is Nᴏᴛ A Sᴜᴘᴘᴏʀᴛᴇᴅ Fɪʟᴇ Fᴏʀᴍᴀᴛ')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('Fɪʟᴇ Is Sᴜᴄᴄᴇsғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ')
    else:
        await msg.edit('Fɪʟᴇ Nᴏᴛ Fᴏᴜɴᴅ Iɴ Dᴀᴛᴀʙᴀsᴇ')
@Client.on_message(filters.command('about'))
async def bot_info(bot, message):
    buttons = [
        [
            InlineKeyboardButton('👥 Oᴜʀ Gʀᴏᴜᴘ', url='https://t.me/askmecinema'),
            InlineKeyboardButton('Sᴏᴜʀᴄᴇ Cᴏᴅᴇ', url='https://t.me/AdhavaaBiriyaniKittiyalo')
        ]
        ]
    await message.reply(text="<b>○ Mʏ ɴᴀᴍᴇ : Tᴏᴠɪɴᴏ Tʜᴏᴍᴀs/n○ Cʀᴇᴀᴛᴏʀ : <a href='https://t.me/stephennedumpally'>JOEL</a>\n○ Cʀᴇᴅɪᴛs: @subinps @MuFaZTG @J_I_S_I_N @Thehellruler @DarkzzAngel\n○ Lᴀɴɢᴜᴀɢᴇ : <code>Pʜʏᴛʜᴏɴ3</code>\n○ Lɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ Aᴄʏɴᴄɪᴏ</a>\n○ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ : <a href='https://t.me/AdhavaaBiriyaniKittiyalo'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>\n○ Sᴇʀᴠᴇʀ : <a href='https://herokuapp.com/'>Hᴇʀᴏᴋᴜ</a>\n○ Dᴀᴛᴀʙᴀsᴇ : <a href='https://www.mongodb.com/'>MᴏɴɢᴏDB</a> </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
