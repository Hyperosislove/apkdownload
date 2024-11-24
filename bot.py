import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Function to fetch APK from Aptoide
def fetch_from_aptoide(app_name: str) -> str:
    """
    Fetch APK download link from Aptoide.

    :param app_name: Name of the app to search for
    :return: APK download link or error message
    """
    # Aptoide API endpoint
    api_url = f"https://ws75.aptoide.com/api/7/app/search?query={app_name}&lang=en"

    try:
        # Make the request to the Aptoide API
        response = requests.get(api_url)
        if response.status_code != 200:
            return "Error: Unable to access Aptoide."

        # Parse the JSON response
        data = response.json()

        # Check if apps are found
        if "datalist" in data and "list" in data["datalist"] and len(data["datalist"]["list"]) > 0:
            # Get the first app in the results
            app = data["datalist"]["list"][0]
            app_name = app["name"]
            apk_link = app["file"]["path"]  # Direct APK download link

            return f"✅ Found '{app_name}'!\nDownload your APK here: {apk_link}"
        else:
            return "Error: App not found on Aptoide."
    except Exception as e:
        return f"Error: Failed to fetch data from Aptoide. Details: {str(e)}"

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the APK Bot!\n"
        "Send me the name of any app, and I'll fetch its APK link for you."
    )

# Handle app name messages
def send_apk(update: Update, context: CallbackContext) -> None:
    app_name = update.message.text.strip()

    # Fetch from Aptoide
    aptoide_result = fetch_from_aptoide(app_name)

    # Respond with the result
    update.message.reply_text(aptoide_result)

# Main function to start the bot
def main() -> None:
    # Your bot token (replace with your own)
    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

    # Set up the Updater and Dispatcher
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_apk))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Run the bot
if __name__ == "__main__":
    main()
