import requests
from telegram import Update
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from dotenv import load_dotenv
import os
from telegram.ext import Updater, CommandHandler, CallbackContext,Application
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    filters,
)

# Replace 'your_bot_token_here' with your actual Telegram bot token

load_dotenv()
# print(os.environ['BOT_TOKEN'])
TELEGRAM_BOT_TOKEN = os.environ['BOT_TOKEN']
# Replace 'http://yourdomain.com/your-app-name/api/albums/' with your actual DRF API endpoint
DRF_API_URL = 'http://127.0.0.1:8000/api/albums/'

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    await update.message.reply_text(
        "I am your Album selling bot use /album for albums"
    )

async def albums(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(DRF_API_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        albums_data = response.json()

        if not albums_data:
            await update.message.reply_text(
                "No album found! Please check the server."
            )
            # context.bot.send_message(chat_id=update.message.chat_id, text="No albums found.")
            return

        for album in albums_data:
            album_name = album.get('name', 'Unknown Album')
            album_id =album.get('id', 'ID')
            release_date = album.get('release_date', 'Unknown Date')
            language = album.get('language', 'Unknown Language')
            artist_name = album.get('artist', {}).get('username', 'Unknown Artist') if isinstance(album.get('artist'), dict) else 'Unknown Artist'
            album_art_url = album.get('album_art', '')
            keyboard = [InlineKeyboardButton("Open Album",callback_data=f"open_album:{album_id}"),
                      ],[InlineKeyboardButton("Buy Local", callback_data=f"buy_local:{album_id}"), InlineKeyboardButton("Buy Globally", callback_data=f"buy_global:{album_id}")]
            
            # open_album_button = InlineKeyboardButton("Open Album", callback_data=f"open_album:{album_id}")
            # buy_local_button = InlineKeyboardButton("Buy Local", callback_data=f"buy_local:{album_id}")
            # buy_global_button = InlineKeyboardButton("Buy Globally", callback_data=f"buy_global:{album_id}")
            # keyboard = [[open_album_button],[buy_local_button],[buy_global_button]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await  update.message.reply_photo(
                photo='https://m.media-amazon.com/images/I/41rH0GN05yL._UXNaN_FMjpg_QL85_.jpg',
                caption=f"{album_name} by {artist_name}\nRelease Date: {release_date}\nLanguage: {language}",
                reply_markup=reply_markup
            )
            # context.bot.send_message(chat_id=update.message.chat_id, text=f"{album_name} by {artist_name}")

    except Exception as e:
        await update.message.reply_text(
            f"Error: {str(e)}"
        )
        # context.bot.send_message(chat_id=update.message.chat_id, text=f"Error: {str(e)}")


async def open_album(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Extract the album ID from the callback data
    album_id = int(query.data.split(":")[1])
    try:
    # Fetch the track list for the given album ID (modify this based on your model structure)
        tracks_response = requests.get(f"{DRF_API_URL}{album_id}/tracks")
        tracks_data = tracks_response.json()
        track_list_message = ""
        if isinstance(tracks_data, list):
            # Create a message with the track list
            for track in tracks_data:
                # Assuming track is a dictionary with a 'name' key
                track_name = track.get('name', 'Unknown Track')
                track_list_message += f"{track_name}\n"
                audio_file_url = track.get('sample', '')
                query.edit_message_text(text=f"{track_name}")
                await context.bot.send_audio(chat_id=query.from_user.id, audio=audio_file_url, title=track_name)
                # await play_audio(query.message.chat.id, audio_file_url)
                    
        else:
            raise ValueError("Invalid response format.")
        
        # Send the track list to the user
        query.edit_message_text(
            text=(f"Album Tracks\n\n{track_list_message}") + "\n\nBack",  
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close")],  
            ]) 
        )



                # track_list_message += track.get('sample','sample')
        # Send the track list message
        # await update.message.reply_text("HI")
        # await context.bot.send_audio(chat_id=query.from_user.id, text=track_list_message,audio=audio_file_url)

        # Send a toast message to the user
        await context.bot.answer_callback_query(callback_query_id=query.id, text="Album opened successfully!")
    except Exception  as e:
        await context.bot.send_message(chat_id=query.from_user.id,
            text=f"Error: {str(e)}"
        )


async def button(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    # Extract the album ID from the callback data
    option = query.data.split(":")[0]
    album_id = int(query.data.split(":")[1])
    await query.answer()
    if option == "open_album":
        await open_album(context=context, update=update)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # simple start function
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("album", albums))
    # Add command handler to start the payment invoice
   
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
