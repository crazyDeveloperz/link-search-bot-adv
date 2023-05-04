from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.group & filters.command("verify"))
async def _verify(bot, message):
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
    except:     
       return await bot.leave_chat(message.chat.id)  
    try:       
       user = await bot.get_users(user_id)
    except:
       return await message.reply(f"❌ {user_name} ɴᴇᴇᴅ ᴛᴏ sᴛᴀʀᴛ ᴍᴇ ɪɴ ᴘᴍ ↬")
    if message.from_user.id != user_id:
       return await message.reply(f"ᴏɴʟʏ {user.mention} ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ☄")
    if verified==True:
       return await message.reply("ᴛʜɪs ɢʀᴏᴜᴘ ɪs ᴀʟʀᴇᴀᴅʏ ᴠᴇʀɪғɪᴇᴅ ♙")
    try:
       link = (await bot.get_chat(message.chat.id)).invite_link     
    except:
       return message.reply("❌ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ʜᴇʀᴇ ᴡɪᴛʜ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs!")    
           
    text  = f"#NewRequest\n\n"
    text += f"User: {message.from_user.mention}\n"
    text += f"User ID: `{message.from_user.id}`\n"
    text += f"Group: [{message.chat.title}]({link})\n"
    text += f"Group ID: `{message.chat.id}`\n"
   
    await bot.send_message(chat_id=LOG_CHANNEL,
                           text=text,
                           disable_web_page_preview=True,
                           reply_markup=InlineKeyboardMarkup(
                                                 [[InlineKeyboardButton("⋞ ᴀᴘᴘʀᴏᴠᴇ ⋟", callback_data=f"verify_approve_{message.chat.id}"),
                                                   InlineKeyboardButton("ℵ ᴅᴇᴄʟɪɴᴇ ℵ", callback_data=f"verify_decline_{message.chat.id}")]]))
    await message.reply("ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜᴇsᴛ sᴇɴᴛ ✅\nᴡᴇ ᴡɪʟʟ ɴᴏᴛɪғʏ ʏᴏᴜ ᴘᴇʀsᴏɴᴀʟʟʏ ᴡʜᴇɴ ɪᴛ ɪs ᴀᴘᴘʀᴏᴠᴇᴅ")


@Client.on_callback_query(filters.regex(r"^verify"))
async def verify_(bot, update):
    id = int(update.data.split("_")[-1])
    group = await get_group(id)
    name  = group["name"]
    user  = group["user_id"]
    if update.data.split("_")[1]=="approve":
       await update_group(id, {"verified":True})
       await bot.send_message(chat_id=user, text=f"ʏᴏᴜʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜᴇsᴛ ғᴏʀ {name} ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ ✅")
       await update.message.edit(update.message.text.html.replace("#NewRequest", "#Approved"))
    else:
       await delete_group(id)
       await bot.send_message(chat_id=user, text=f"ʏᴏᴜʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜᴇsᴛ ғᴏʀ {name} ʜᴀs ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ 😐 ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ")
       await update.message.edit(update.message.text.html.replace("#NewRequest", "#Declined"))
