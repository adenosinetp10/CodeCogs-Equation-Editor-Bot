from configparser import ConfigParser
from telegram.ext import Updater, Defaults, Filters
from telegram import ParseMode
import logging
from bot import start, msg_latex, inline_latex

from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='codecogs_latex.log')



def main() -> None:
    
    config = ConfigParser()
    config.read('config.ini')

    token = config['bot']['token']


    defaults = Defaults(parse_mode=ParseMode.MARKDOWN_V2, run_async=True)
    
    updater = Updater(token=token, defaults=defaults)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, msg_latex))
    dp.add_handler(InlineQueryHandler(inline_latex, pass_user_data=True))

    updater.start_polling()
    updater.idle()
    


if __name__ == '__main__':
    
    main()