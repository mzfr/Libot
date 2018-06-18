import logging
import Lichess
import telegram
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "Your bot token"

URL = " https://lichess.org/api/"


def start(bot, update):
    """Send a message when the command /start is given"""
    update.message.reply_text("Hello")


def help(bot, update):
    """sends a message when the command /help is given"""
    update.message.reply_text(
        'These are the commands you can use\n'
        '/start - Greets you with Hello\n'
        '/help - Display available commands\n'
        '/profile <username> - Display information about a lichess user\n'
        '/online <username(s), separated by comma> - Check if user(s) \
            are online or not\n'
        '/top <chess variant> - Display top 10 player for particular variant\n'
        '/stream - Display all live streamer on lichess\n'

    )


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def user(bot, update, args):
    """Return information about a particular user of lichess.org"""
    profile = Lichess.profile(args)
    update.message.reply_text(profile, parse_mode=telegram.ParseMode.HTML)


def online(bot, update, args):
    """Check if a particular user is online or not"""
    args = "".join(args)
    online = Lichess.is_online(args)
    update.message.reply_text(online, parse_mode=telegram.ParseMode.HTML)


def top_players(bot, update, args):
    """Get top 10 player for a particular variant"""
    args = "".join(args)
    update.message.reply_text(Lichess.top_players(args),
                              parse_mode=telegram.ParseMode.HTML)


def streamer(bot, update):
    """Get all the active streamer on lichess.org
        along with link to stream
    """
    update.message.reply_text(Lichess.streamers(),
                              parse_mode=telegram.ParseMode.HTML)


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("profile", user, pass_args=True))
    dp.add_handler(CommandHandler("online", online, pass_args=True))
    dp.add_handler(CommandHandler("top", top_players, pass_args=True))
    dp.add_handler(CommandHandler("stream", streamer))
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
