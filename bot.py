import telebot
import requests
import eventlet
import os
import random
# from flask import Flask, request
import util
from telebot import apihelper
import constants
import emoji

# apihelper.proxy = {'https': 'socks5://103.216.82.190:6667'}
bot = telebot.TeleBot(constants.token)
bot.send_message(358886422, u'\U0001F4A8')

types = telebot.types
# server = Flask(__name__)

URL_VK_FEED = 'https://api.vk.com/method/wall.get?owner_id=-126132&count=10&filter=owner'
URL_VK_ALBUMS = 'https://api.vk.com/method/photos.getAlbums?owner_id=-126132&count=10'
URL_VK_PHOTOS = 'https://api.vk.com/method/photos.get?owner_id=-126132&count=50&album_id='
URL_VK_ALBUM = 'https://vk.com/album-126132_'
FILENAME_VK = 'last_known_id.txt'
BASE_POST_URL = 'https://vk.com/wall-126132_'
URL_INST_FEED = 'https://api.instagram.com/v1/users/self/media/recent/?access_token={INSERT_YOUR_TOKEN}&count=10'
URL_HH_LIST = 'https://api.hh.ru/vacancies/?employer_id=4745&period=7&order=employer_active_vacancies_order'
URL_HH_EMP = 'https://spb.hh.ru/employer/4745'

user_history = {}


def get_data(data_type, alb_id):
    timeout = eventlet.Timeout(10)
    try:
        feed = None
        if data_type == 'feed':
            feed = requests.get(URL_VK_FEED)
        elif data_type == 'albums':
            feed = requests.get(URL_VK_ALBUMS)
        elif data_type == 'photos':
            feed = requests.get(URL_VK_PHOTOS + alb_id)
        elif data_type == 'inst':
            feed = requests.get(URL_INST_FEED)
        elif data_type == 'hh':
            feed = requests.get(URL_HH_LIST + alb_id)
        return feed.json()
    except eventlet.timeout.Timeout:
        return None
    finally:
        timeout.cancel()


@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id,
                     "Добрый день, {}! Выберите в меню, что вы хотите посмотреть.".format(message.chat.first_name),
                     reply_markup=util.get_default_markup())


@bot.message_handler(commands=['0000'])
def handle_text(message)
    bot.


@bot.message_handler(regexp="Развозка*")
def handle_text(message):
    bot.send_message(message.chat.id, text=constants.BUS_SCHEDULE,
                     reply_markup=util.get_default_markup())
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Остановки', callback_data='Остановки'))
    bot.send_message(message.chat.id, text='Также посмотрите:', reply_markup=markup)


@bot.message_handler(regexp="Санкт Петербург " + emoji.city1)
def handle_text(message):
    handle_find_dd("Санкт-петербургского офиса", message)


@bot.message_handler(regexp="Москва " + emoji.city1)
def handle_text(message):
    handle_find_dd("Московского офиса", message)


@bot.message_handler(regexp="Саратов " + emoji.city1)
def handle_text(message):
    handle_find_dd("Саратовского офиса", message)


@bot.message_handler(regexp="Санкт Петербург " + emoji.city2)
def handle_text(message):
    bot.send_message(message.chat.id,"OK")
    handle_vacancy("Санкт-Петербург", message)


@bot.message_handler(regexp="Москва " + emoji.city2)
def handle_text(message):
    handle_vacancy("Москва", message)



@bot.message_handler(regexp="Саратов " + emoji.city2)
def handle_text(message):
    handle_vacancy("Саратов", message)


def handle_vacancy(city,message):
    bot.send_chat_action(message.chat.id, action='typing')
    markup = util.work_hh_category(city)
    bot.send_message(message.chat.id, 'Выберите специальность (в скобках указано число вакансий):',
                     reply_markup=markup)
    bot.send_message(message.chat.id, "Что еще хотите узнать?", reply_markup=util.get_default_markup())


def handle_find_dd(text, message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Адрес " + text)
    markup.add("Телефон " + text)
    bot.send_message(message.chat.id, "Что хотите узнать?", reply_markup=markup)


@bot.message_handler(regexp="Адрес *")
def handle_text(message):
    text = message.text
    if text == constants.SPB_ADDRESS:
        bot.send_venue(message.chat.id, latitude=59.947283, longitude=30.255244, title='Digital Design в СПб',
                       address='наб. реки Смоленки, д. 33', reply_markup=util.get_default_markup())
    elif text == constants.SARATOV_ADDRESS:
        bot.send_venue(message.chat.id, latitude=51.583888, longitude=45.964457, title='Digital Design в Саратове',
                       address='проспект 50 лет Октября, д. 107а, офис 703', reply_markup=util.get_default_markup())
    elif text == constants.MOSCOW_ADDRESS:
        bot.send_venue(message.chat.id, latitude=55.679541, longitude=37.622388, title='Digital Design в Москве',
                       address='Варшавское шоссе, д. 36, стр. 8, под. 5, 1 этаж',
                       reply_markup=util.get_default_markup())


@bot.message_handler(regexp="Телефон *")
def handle_text(message):
    text = message.text
    if text == constants.SPB_TEL:
        bot.send_contact(message.chat.id, phone_number='7 (812) 346-58-33', first_name='Digital',
                         last_name='Design (Санкт-Петербург)', reply_markup=util.get_default_markup())
    elif text == constants.SARATOV_TEL:
        bot.send_contact(message.chat.id, phone_number='7 (8452) 983 483', first_name='Digital',
                         last_name='Design (Саратов)', reply_markup=util.get_default_markup())
    elif text == constants.MOSCOW_TEL:
        bot.send_contact(message.chat.id, phone_number='7 (499) 788-74-94', first_name='Digital',
                         last_name='Design (Москва)', reply_markup=util.get_default_markup())


@bot.message_handler(regexp="Найти DD*")
def handle_text(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Санкт Петербург " + emoji.city1)
    markup.add("Москва " + emoji.city1)
    markup.add("Саратов " + emoji.city1)
    bot.send_message(message.chat.id, "Что хотите узнать?", reply_markup=markup)


@bot.message_handler(regexp="Вакансии*")
def handle_text(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Санкт Петербург " + emoji.city2)
    markup.add("Москва " + emoji.city2)
    markup.add("Саратов " + emoji.city2)
    bot.send_message(message.chat.id, "Выберите город", reply_markup=markup)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id,
                     'Добрый день, {}! Выберите в меню, что вы хотите посмотреть.'.format(
                         message.chat.first_name) + constants.HELP,
                     reply_markup=util.get_default_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        try:
            if call.data == 'Остановки':
                bot.send_venue(call.message.chat.id, latitude=59.948205, longitude=30.233737,
                               title='Остановка у метро',
                               address='')
                bot.send_venue(call.message.chat.id, latitude=59.947292, longitude=30.256356,
                               title='Остановка у бизнес центра',
                               address='', reply_markup=util.get_default_markup())
            elif call.data.split('=')[0] == '&specialization':
                spec = call.data
                feed = util.get_data('hh', spec)
                if feed is not None:
                    for i in range(feed['items'].__len__()):
                        target_link = feed['items'][i]['alternate_url']
                        target_text = '<b>' + feed['items'][i]['name'] + '</b>\n' + feed['items'][i]['created_at'][
                                                                                    :10] + '\n' + \
                                      feed['items'][i]['snippet']['responsibility']
                        markup = types.InlineKeyboardMarkup()
                        button = types.InlineKeyboardButton(text='Перейти к вакансии', url=target_link)
                        markup.add(button)
                        bot.send_message(call.message.chat.id, text=target_text, reply_markup=markup,
                                         parse_mode='html')
                markup = types.InlineKeyboardMarkup()
        except Exception as ex:
            print('Exception of type {!s}: {!s}'.format(type(ex).__name__, str(ex)))
            pass


bot.polling(none_stop=True, timeout=0)
# @server.route("/bot", methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200
#
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url="https://test-tb.herokuapp.com/bot")
#     return "!", 200


# server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
# server = Flask(__name__)
