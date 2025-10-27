from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8320626110:AAECTdSq8aTdmoEpfGGz8oPtRYVR379GBfU"

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    print(f"Chat ID: {chat_id}")
    await update.message.reply_text(f"Il tuo chat_id è {chat_id}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
