import logging
import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Log sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Fayl yo‘llari
BASE_DIR = os.getcwd()  # Pella serverida to‘g‘ri ishchi papka
PDF_PATH = os.path.join(BASE_DIR, "web-hacking-101.pdf")
MP3_PATH = os.path.join(BASE_DIR, "LAG.mp3")

# Menyu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("/start")],
        [KeyboardButton("/help")],
        [KeyboardButton("📘 Web Hacking 101 (PDF)")],
        [KeyboardButton("🎧 LAG Audio (MP3)")]
    ],
    resize_keyboard=True
)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n"
        "Men sizga Web Hacking asoslarini o‘rgatuvchi Telegram botman.\n"
        "Quyidagi menyudan tanlang:",
        reply_markup=main_menu
    )

# /help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Yordam:\n"
        "- /start – Botni ishga tushurish\n"
        "- 📘 Web Hacking 101 (PDF) – Darslikni olish\n"
        "- 🎧 LAG Audio (MP3) – ⚠️ Telefoningizni qotirib qo‘yishi mumkin. Ehtiyot bo‘ling!",
        reply_markup=main_menu
    )

# PDF yuborish
async def send_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(PDF_PATH):
        await update.message.reply_document(
            document=open(PDF_PATH, 'rb'),
            filename="web-hacking-101.pdf",
            caption="📘 Web Hacking 101 darsligi"
        )
    else:
        await update.message.reply_text("❌ PDF fayl topilmadi.")

# MP3 yuborish
async def send_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(MP3_PATH):
        await update.message.reply_audio(
            audio=open(MP3_PATH, 'rb'),
            filename="LAG.mp3",
            caption=(
                "⚠️ Diqqat!\n"
                "Bu fayl \"LAG.mp3\" telefoningizni qotirib qo‘yishi mumkin.\n"
                "📵 Iltimos ehtiyotkorlik bilan oching!"
            )
        )
    else:
        await update.message.reply_text("❌ MP3 fayl topilmadi.")

# Botni ishga tushurish
if __name__ == '__main__':
    TOKEN = "8047527349:AAGpapBscX-I0WYvzbbU79nd675JPHG9-tI"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Web Hacking 101"), send_pdf))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("LAG Audio"), send_mp3))

    print("✅ Bot menyu bilan ishga tushdi...")
    app.run_polling()
