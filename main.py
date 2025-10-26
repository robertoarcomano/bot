from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from http import HTTPStatus
from contextlib import asynccontextmanager

TOKEN = "8320626110:AAHNT5MxFx3H_t8-YXe6KaTMXQ2klP_9l2s"
WEBHOOK_URL = "https://api.robertoarcomano.com/webhook"  # URL esposto pubblicamente

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

@app.post("/webhook")
async def process_update(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono un bot FastAPI minimal.")

bot_app.add_handler(CommandHandler("start", start))
