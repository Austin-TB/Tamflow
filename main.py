import os
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from telegram import MessageEntity
from dotenv import load_dotenv
import asyncio
from workflow import start_worfklow
from crawler import fetch_article_markdown

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
allowed_users = set(os.getenv("WHITELIST","").split(","))
async def handler(update, context):
    if str(update.message.from_user.id) not in allowed_users:
        await update.message.reply_text("Unauthorized user")
        return
    
    text = update.message.text

    #check if user messages contain URL or article content
    urls = update.message.parse_entities(types=[MessageEntity.URL])

    user = update.message.from_user.first_name
    msg = await update.message.reply_text("Processing your input...")

    if urls:
        
        response = await parse_and_summarize(list(urls.values()))
    else:
        response = await summarize(text)

    await msg.edit_text(response)

async def parse_and_summarize(urls):
    text = await fetch_article_markdown(urls[0])
    summary = start_worfklow(text)
    return summary

async def summarize(text):
    summary = start_worfklow(text)
    return summary

def main():
    print("Starting the bot...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handler))
    app.add_handler(CommandHandler("start", handler))
    print("Bot is live")
    app.run_polling()


if __name__ == "__main__":
    main()
