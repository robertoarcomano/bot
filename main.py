from fastapi import FastAPI, Request, Response, Header
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters
from http import HTTPStatus
from contextlib import asynccontextmanager
import os
import asyncio

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://api.robertoarcomano.com:8443/webhook"  # URL esposto pubblicamente
bot_app = (
    Application.builder()
    .token(TOKEN)
    .build()
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot_app.bot.setWebhook(WEBHOOK_URL)
    async with bot_app:
        await bot_app.start()
        yield
        await bot_app.stop()

app = FastAPI(lifespan=lifespan)

@app.post("/trigger-pull")
async def trigger_pull(request: Request, authorization: str = Header(None)):
    # Sicurezza: controlla un token segreto
    if authorization != f"Bearer {os.getenv('REPOSITORY_SECRET')}":
        return Response(status_code=HTTPStatus.UNAUTHORIZED)
    repo_path = "/home/berto/bot"
    try:
        process = await asyncio.create_subprocess_exec(
            "git", "pull",
            cwd=repo_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
    except Exception:
        return Response(status_code=HTTPStatus.UNAUTHORIZED)
    return {"status": "pull eseguito", "message": stdout.decode()}

@app.post("/webhook")
async def process_update(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono un bot FastAPI minimal.")

async def go1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("go1!")

async def pull(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo_path = "/home/berto/bot"
    try:
        process = await asyncio.create_subprocess_exec(
            "git", "pull",
            cwd=repo_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
          await update.message.reply_text(f"not pulled: {stderr.decode()}")
        else:
          await update.message.reply_text(f"pulled: {stdout.decode()}")
    except Exception as e:
        await update.message.reply_text(f"not pulled: {str(e)}")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    print(f"Chat ID: {chat_id}")
    await update.message.reply_text(f"Il tuo chat_id è {chat_id}")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("test")

async def test5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("test5")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("go1", go1))
bot_app.add_handler(CommandHandler("pull", pull))
bot_app.add_handler(CommandHandler("getchatid", get_chat_id))
bot_app.add_handler(CommandHandler("test", test))
bot_app.add_handler(CommandHandler("test5", test5))
