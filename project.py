from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import dotenv_values
import spotify_api as api

config = dotenv_values('.env')

TOKEN: Final = config['BOT_TOKEN']
BOT_USERNAME: Final = config['BOT_USERNAME']

def main():
    activate_bot()

def activate_bot():
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)



def handle_response(text: str) -> str:
    # get auth token
    token = api.get_token()

    # response logic
    processed: str = text.lower()

    if processed.startswith('-artist'):
        # remove prefix
        artist_name = processed[len('-artist'):].strip()

        # get artist id
        artist_id = api.get_artist_id(token, artist_name)
        
        # validation check
        if artist_id == 'not found':
            return f'Sorry we couldn\'t find the artist you were looking for!'
        
        # get artist link
        artist_link = api.get_artist_link(token, artist_id)

        return artist_link

    elif processed.startswith('-song'):
        # remove prefix
        song_name = processed[len('-song'):].strip()

        # get song id
        song_id = api.get_song_id(token, song_name)

        # validation check
        if song_id == 'not found':
            return f'Sorry we couldn\'t find the song you were looking for!'
        
        # get song link
        song_link = api.get_song_link(token, song_id)

        return song_link
    
    elif processed.startswith('-album'):
        # remove prefix
        album_name = processed[len('-album'):].strip()

        # get album id
        album_id = api.get_album_id(token, album_name)

        # validation check
        if album_id == 'not found':
            return f'Sorry we couldn\'t find the album you were looking for!'
        
        # get album link
        album_link = api.get_album_link(token, album_id)

        return album_link

    return 'Type /help for the usage of Sharify!'



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! This is Sharify! Easily share song information on Telegram with friends! Type /help for the usage of Sharify!')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type -artist <ArtistName> to get a specific artist link on Spotify!\nType -song <SongName> to get a specific song link on Spotify!\nType -album <AlbumName> to get a specific album link on Spotify!')

# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    main()