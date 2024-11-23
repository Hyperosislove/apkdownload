import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Function to fetch APK download link
def fetch_apk(apk_name: str) -> str:
    base_url = "https://apkpure.com/search?q="  # Example website
    search_url = base_url + apk_name.replace(" ", "+")
    
    response = requests.get(search_url)
    if response.status_code != 200:
        return "Error: Unable to access the website."

    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find('a', {'class': 'dd'})
    
    if link:
        apk_page_url = "https://apkpure.com" + link['href']
        apk_response = requests.get(apk_page_url)
        apk_soup = BeautifulSoup(apk_response.content, 'html.parser')
        download_link = apk_soup.find('a', {'class': 'download-start-btn'})['href']
        return download_link
    else:
        return "Error: APK not found."

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me the name of the APK, and I'll fetch it for you.")

async def handle_apk_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apk_name = update.message.text
    await update.message.reply_text(f"Searching for APK: {apk_name}...")
    
    download_link = fetch_apk(apk_name)
    if "Error" in download_link:
        await update.message.reply_text(download_link)
    else:
        await update.message.reply_text(f"Download your APK here: {download_link}")

# Main function to start the bot
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Add your bot token here
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_apk_request))

    application.run_polling()

if __name__ == "__main__":
    main()
