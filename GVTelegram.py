from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import Getmovie
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CINEMA, MOVIE, DATE, CHECKSPECIFIC = range(4)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
def movie(bot, update):
    # reply_keyboard = [['Boy', 'Girl', 'Other']]
    cinemaname = Getmovie.cinemalist()
    button_list = [KeyboardButton(s) for s in cinemaname]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=1), one_time_keyboard=True, selective=True)
    update.message.reply_text(
        'Which cinema?',
        reply_markup=reply_markup)

    return CINEMA


def cinema(bot, update, user_data):
    user = update.message.from_user
    text = update.message.text
    user_data['cinemaname'] = text
    user_data['cinemaid'] = Getmovie.getcinemaid(text.lower())
    update.message.reply_text('So you want to watch at {}'.format(text))
    cinemaname = Getmovie.showingincinemalist(user_data['cinemaid'])
    if str(cinemaname) != '[]':
        button_list = [KeyboardButton(s) for s in cinemaname]
        reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=1), one_time_keyboard=True, selective=True)
        update.message.reply_text(
            'Which movie?',
            reply_markup=reply_markup)

        return MOVIE
    else:
        update.message.reply_text(
            'No movie found in this cinema')
        return ConversationHandler.END

def moviedetail(bot, update, user_data):
    user = update.message.from_user
    text = update.message.text
    user_data['moviename'] = text
    user_data['movieid'] = Getmovie.getshowingincinemaid(cinemaId=user_data['cinemaid'], filmTitle=text.lower())
    update.message.reply_text('{}?\nAlright.'.format(text),
                              reply_markup=ReplyKeyboardRemove())
    datelist = Getmovie.showingincinemadatelist(user_data['cinemaid'], user_data['movieid'])
    button_list = [KeyboardButton(s) for s in datelist]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=1), one_time_keyboard=True, selective=True)
    update.message.reply_text(
        'Which day?',
        reply_markup=reply_markup)

    return DATE

def date(bot, update, user_data):
    user = update.message.from_user
    text = update.message.text
    # user_data['movieid'] = Getmovie.getshowingincinemaid(cinemaId=user_data['cinemaid'], filmTitle=text.lower())
    update.message.reply_text('On {}? OK!'.format(text),
                              reply_markup=ReplyKeyboardRemove())
    user_data['date'] = Getmovie.getunixdate(text)
    user_data['datetext'] = text
    sessions, keyboard, thedetails = Getmovie.getsessioninfo(cinemaId=user_data['cinemaid'], filmCode=user_data['movieid'], showDate=user_data['date'])
    user_data['thedetails'] = thedetails
    button_list = [KeyboardButton(s) for s in keyboard]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=1), one_time_keyboard=True, selective=True)
    update.message.reply_text('Here are the details\nCinema: {}\nMovie: {}\nDate: {}\n\n{}'.format(user_data['cinemaname'], user_data['moviename'], user_data['datetext'], "\n".join(sessions)), reply_markup=reply_markup)
    return CHECKSPECIFIC

def checkspecific(bot, update, user_data):
    user = update.message.from_user
    text = update.message.text
    # user_data['movieid'] = Getmovie.getshowingincinemaid(cinemaId=user_data['cinemaid'], filmTitle=text.lower())
    update.message.reply_text('At {}? OK!'.format(text),
                              reply_markup=ReplyKeyboardRemove())
    sessions, keyboard, thedetails = Getmovie.getsessioninfo(cinemaId=user_data['cinemaid'], filmCode=user_data['movieid'], showDate=user_data['date'])
    user_data['thedetails'] = thedetails
    for i in thedetails:
        if i['time12'] == text:
            user_data['time24'] = i['time24']
            user_data['hallNumber'] = i['hallNumber']
    update.message.reply_text('Here are the details\n{}'.format(Getmovie.checkseatsdetail(cinemaId=user_data['cinemaid'],filmCode=user_data['movieid'],showDate=user_data['date'],showTime=user_data['time24'],hallNumber=user_data['hallNumber'])), reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
    

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text("""Awww, Don't want to watch movie anymore? :(""",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("830974716:AAGFe0o-De0apRzxHFTl-uNPSN0ikO1U_MI")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('movie', movie)],

        states={
            CINEMA: [MessageHandler(Filters.text, cinema, pass_user_data=True)],
            MOVIE: [MessageHandler(Filters.text, moviedetail, pass_user_data=True)],
            DATE: [MessageHandler(Filters.text, date, pass_user_data=True)],
            CHECKSPECIFIC: [MessageHandler(Filters.text, checkspecific, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
