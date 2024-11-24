import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Function to fetch APK download link from APKPure
def fetch_from_apkpure(apk_name: str) -> str:
    base_url = "https://apkpure.com/search?q="
    search_url = base_url + apk_name.replace(" ", "+")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first search result link
    link = soup.find('a', class_="more-down")  # Updated selector
    if link:
        apk_page_url = "https://apkpure.com" + link['href']

        # Fetch the APK page
        apk_response = requests.get(apk_page_url, headers=headers)
        apk_soup = BeautifulSoup(apk_response.content, 'html.parser')

        # Find the download button
        download_button = apk_soup.find('a', id="download_link")  # Updated selector
        if download_button and 'href' in download_button.attrs:
            return download_button['href']
    return None

# Function to fetch APK download link from APKMirror
def fetch_from_apkmirror(apk_name: str) -> str:
    base_url = "https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s="
    search_url = base_url + apk_name.replace(" ", "+")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first search result link
    link = soup.find('a', class_="fontBlack")  # Updated selector
    if link:
        apk_page_url = "https://www.apkmirror.com" + link['href']

        # Fetch the APK page
        apk_response = requests.get(apk_page_url, headers=headers)
        apk_soup = BeautifulSoup(apk_response.content, 'html.parser')

        # Find the download button
        download_button = apk_soup.find('a', class_="downloadButton")  # Updated selector
        if download_button and 'href' in download_button.attrs:
            return "https://www.apkmirror.com" + download_button['href']
    return None

# Master function to try fetching APK from multiple sources
def fetch_apk(apk_name: str) -> str:
    # Try APKPure first
    download_link = fetch_from_apkpure(apk_name)
    if download_link:
        return f"APK found on APKPure: {download_link}"

    # Try APKMirror next
    download_link = fetch_from_apkmirror(apk_name)
    if download_link:
        return f"APK found on APKMirror: {download_link}"

    # Add more sources as needed
    return "Error: APK not found on any supported website."

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me the name of the APK, and I'll fetch it for you from trusted sources.")

async def handle_apk_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apk_name = update.message.text
    await update.message.reply_text(f"Searching for APK: {apk_name}...")

    download_link = fetch_apk(apk_name)
    await update.message.reply_text(download_link)

# Main function to start the bot
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Add your bot token here
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_apk_request))

    application.run_polling()

if __name__ == "__main__":
    main()
