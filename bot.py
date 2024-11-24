import os
import requests
from google_play_scraper import search
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Function to get package name using Google Play Scraper
def get_package_name(app_name: str) -> str:
    results = search(app_name, lang="en", country="us")
    if results:
        return results[0]['appId']
    return None

# Function to fetch APK download link from APKCombo
def fetch_from_apkcombo(package_name: str) -> str:
    base_url = "https://apkcombo.com/downloader/apk/"
    params = {
        "package": package_name,
        "lang": "en",
        "dpi": "nodpi"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        return "Error: Unable to access APKCombo."

    if "Download APK" in response.text:
        return response.url
    else:
        return "Error: APK not found."

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me the name of the APK, and I'll fetch it for you.")

async def handle_apk_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apk_name = update.message.text
    await update.message.reply_text(f"Searching for APK: {apk_name}...")

    # Step 1: Get package name
    package_name = get_package_name(apk_name)
    if not package_name:
        await update.message.reply_text("Error: Could not find package name.")
        return

    # Step 2: Fetch APK download link
    download_link = fetch_from_apkcombo(package_name)
    await update.message.reply_text(download_link)

# Main function to start the bot
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Add your Telegram bot token here
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_apk_request))

    application.run_polling()

if __name__ == "__main__":
    main()
