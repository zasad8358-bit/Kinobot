import json
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8365272312:AAH4jaSNaQ95t_Tn2P_KjMvcqBsWXXzmHuM"

FAYL = "kinolar.json"

def load():
    if os.path.exists(FAYL):
        with open(FAYL, "r") as f:
            return json.load(f)
    return {}

def save(data):
    with open(FAYL, "w") as f:
        json.dump(data, f)

kinolar = load()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Kino botga xush kelibsiz!\n\nKino raqamini yuboring!")

async def kanal_kino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.channel_post
    if msg and msg.video:
        kod = str(len(kinolar) + 1)
        kinolar[kod] = msg.video.file_id
        save(kinolar)
        await context.bot.send_message(
            chat_id=msg.chat.id,
            text=f"✅ Kino saqlandi! Kod: {kod}"
        )

async def kino_ber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kod = update.message.text.strip()
    if kod in kinolar:
        await update.message.reply_video(
            video=kinolar[kod],
            caption=f"🎬 Kino kodi: {kod}"
        )
    else:
        await update.message.reply_text("❌ Bunday kodli kino topilmadi!")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO & filters.ChatType.CHANNEL, kanal_kino))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kino_ber))
app.run_polling(allowed_updates=["message", "channel_post"])
