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
    await update.message.reply_text("🎬 Kino botga xush kelibsiz!\n\nKino kodini yuboring!")

async def kanal_kino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.channel_post
    if msg and msg.video:
        kod = str(len(kinolar) + 1)
        caption = msg.caption or ""
        kinolar[kod] = {
            "file_id": msg.video.file_id,
            "tavsif": caption
        }
        save(kinolar)
        await context.bot.send_message(
            chat_id=msg.chat.id,
            text=f"✅ Kino saqlandi! Kod: {kod}"
        )

async def kino_ber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kod = update.message.text.strip()
    if kod in kinolar:
        kino = kinolar[kod]
        tavsif = kino.get("tavsif", "")
        caption = f"🎬 Kino kodi: {kod}"
        if tavsif:
            caption += f"\n\n{tavsif}"
        await update.message.reply_video(
            video=kino["file_id"],
            caption=caption
        )
    else:
        await update.message.reply_text("❌ Bunday kodli kino topilmadi!")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO & filters.ChatType.CHANNEL, kanal_kino))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kino_ber))
app.run_polling(allowed_updates=["message", "channel_post"])
