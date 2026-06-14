import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import httpx
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hegidiya Maga!,GURU edini.Yen beku?")

async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_message=update.message.text
    async with httpx.AsyncClient(timeout=180) as client:
            response= await client.post("http://localhost:8000/chat",json={"content":user_message})


    data=response.json()
    await update.message.reply_text(data["response"])

def main():
    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))

    print("Wait madu Yochane Madi Heltini...")
    app.run_polling()
    print(f"DEBUG: Token loaded is: {TOKEN[:10]}...") 
if __name__=="__main__":
    main()

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env file!")