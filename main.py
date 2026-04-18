import os
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from telegram import MessageEntity
from dotenv import load_dotenv
import asyncio

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
    await asyncio.sleep(3)
    return f"This is the summary after parsing the urls {urls}"

async def summarize(text):
    await asyncio.sleep(1)
    return "This is the summary of the text"

def main():
    print("Starting the bot...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handler))
    app.add_handler(CommandHandler("start", handler))
    print("Bot is live")
    app.run_polling()


if __name__ == "__main__":
    main()
