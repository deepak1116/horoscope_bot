from telebot import TeleBot
from telebot import types
import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime,tzinfo,timedelta

API_KEY = 'APIKEY'
bot = TeleBot(API_KEY, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_first_name = str(message.chat.first_name)
    bot.send_message(message.chat.id,"Welcome "+user_first_name + "\nReady to see daily horoscope!.\nPLease execute /horoscope")


@bot.message_handler(commands=['horoscope'])
def send_horoscope_home_page(message):
    button_aries = types.InlineKeyboardButton('Aries', callback_data='Aries')
    button_taurus = types.InlineKeyboardButton('Taurus', callback_data='Taurus')
    button_gemini = types.InlineKeyboardButton('Gemini', callback_data='Gemini')
    button_cancer = types.InlineKeyboardButton('Cancer', callback_data='Cancer')
    button_leo = types.InlineKeyboardButton('Leo', callback_data='Leo')
    button_vigro = types.InlineKeyboardButton('Virgo', callback_data='Virgo')
    button_libra = types.InlineKeyboardButton('Libra', callback_data='Libra')
    button_scorpio = types.InlineKeyboardButton('Scorpio', callback_data='Scorpio')
    button_sagittarius = types.InlineKeyboardButton('Sagittarius', callback_data='Sagittarius')
    button_capricorn = types.InlineKeyboardButton('Capricorn', callback_data='Capricorn')
    button_aquarius = types.InlineKeyboardButton('Aquarius', callback_data='Aquarius')
    button_pisces = types.InlineKeyboardButton('Pisces', callback_data='Pisces')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_aries,button_taurus)
    keyboard.add(button_gemini,button_cancer)
    keyboard.add(button_leo,button_vigro)
    keyboard.add(button_libra,button_scorpio)
    keyboard.add(button_sagittarius,button_capricorn)
    keyboard.add(button_aquarius,button_pisces)

    bot.send_message(message.chat.id,"Select your zodiac sign for daily Horscope.",reply_markup=keyboard)
    bot.get_my_commands()


# @bot.callback_query_handler(lambda query: query.data == "aries")
@bot.callback_query_handler(lambda query: True)
def horoscope_callback_query(query):
    zodiac_sign_dic = {'aries': 1, 'taurus': 2, 'gemini': 3,
           'cancer': 4, 'leo': 5, 'virgo': 6,
           'libra': 7, 'scorpio': 8, 'sagittarius': 9,
           'capricorn': 10, 'aquarius': 11, 'pisces': 12}
    zodiac_sign = 0
    zodiac_name = query.data
    if zodiac_name.lower() in zodiac_sign_dic.keys():
        zodiac_sign = zodiac_sign_dic.get(zodiac_name.lower())
        daily_horoscope = get_horoscope_data(zodiac_sign,zodiac_name)
    bot.send_message(query.message.chat.id,daily_horoscope)



def get_horoscope_data(zodiac_sign,zodiac_name):
    horoscope_dictionary = horoscope_scrapper(zodiac_sign)
    horoscope_today_date = horoscope_dictionary.get("today")[0]
    date_diff = check_date(horoscope_today_date)
    result = "Some error occured"
    if date_diff < 0:
        result = "Sign: " + zodiac_name+"\n\n"+horoscope_dictionary.get("tomorrow")[1]
        print("called tomorrow")
    else:
        result = "Sign: " + zodiac_name+"\n\n"+horoscope_dictionary.get("today")[1]
        print("called today")

    return result

def horoscope_scrapper(zodiac_sign):
    url_today = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-today.aspx?sign={zodiac_sign}"
    )
    url_tomorrow = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-tomorrow.aspx?sign={zodiac_sign}"
    )
    soup_today = BeautifulSoup(requests.get(url_today).content, "html.parser")
    soup_tomorrow = BeautifulSoup(requests.get(url_tomorrow).content, "html.parser")

    # print(soup.find("div", class_="main-horoscope").p.text)
    horoscope_today = [soup_today.find("div", class_="main-horoscope").p.strong.text,
                       soup_today.find("div", class_="main-horoscope").p.text]
    horoscope_tomorrow = [soup_tomorrow.find("div", class_="main-horoscope").p.strong.text,
                          soup_tomorrow.find("div", class_="main-horoscope").p.text]
    horoscope_dict = {
        "today": horoscope_today,
        "tomorrow": horoscope_tomorrow
    }
    return horoscope_dict

def check_date(date_str):
    IST =  pytz.timezone('Asia/Kolkata')
    # date_str = 'Dec 9, 2023
    horoscope_date_today = datetime.strptime(date_str, '%b %d, %Y').date()
    IST_date_today = datetime.now(IST).date()
    date_diff = horoscope_date_today - IST_date_today
    return date_diff.days


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    error_message = ("Oops, please refer below available commands. \n"+
                    "1./start \n" +
                    "2./horoscope \n"+
                    "3./help \n")
    bot.reply_to(message, error_message)

if __name__ == '__main__':
        bot.polling(none_stop=True)
