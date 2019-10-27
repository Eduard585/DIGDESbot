"""
Служебные функции для работы с приложением
"""
import eventlet
import requests
import time
import telebot
import datetime
import constants
types = telebot.types


def get_data(type, alb_id):
    timeout = eventlet.Timeout(10)
    try:
        if type == 'hh':
            feed = requests.get(constants.URL_HH_LIST+alb_id)
        elif type == 'hh_spec':
            feed = requests.get(constants.URL_HH_SPEC)
        return feed.json()
    except eventlet.timeout.Timeout:
        return None
    finally:
        timeout.cancel()


"""
Подготовка стандартной клавиатуры приложения
"""


def get_default_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Развозка")
    markup.add("Вакансии", "Найти DD")
    return markup


"""
Обработка команды Вакансии (отображение вакансий с hh.ru)
"""


def work_hh(bot, message):
    try:
        feed = get_data('hh', '0')
        if feed is not None:
            for i in range(int(message.text)):
                target_link = feed['items'][i]['alternate_url']
                target_text = '<b>' + feed['items'][i]['name'] + '</b>\n' + feed['items'][i]['created_at'][:10] + '\n' + \
                              feed['items'][i]['snippet']['responsibility']
                markup = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='Перейти к вакансии', url=target_link)
                markup.add(button)
                bot.send_message(message.chat.id, text=target_text, reply_markup=markup, parse_mode='html')
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='hh.ru', url=constants.URL_HH_EMP)
        markup.add(button)
        bot.send_message(message.chat.id, text='Перейти к полному списку вакансий', reply_markup=markup)
    except Exception as ex:
        print('Exception of type {!s}: {!s}'.format(type(ex).__name__, str(ex)))
        pass
    return


"""
Отображение ближайшей развозки
"""


bus_sched = ['8:45', '9:00', '9:15', '9:30', '9:45', '10:00', '18:30', '18:45', '19:00', '19:15', '19:30',
             '19:45', '20:00', '20:20']


def next_bus(bot, message):
    try:
        now = datetime.datetime.fromtimestamp(time.time())
        half_day = datetime.datetime.fromtimestamp(time.time()) - datetime.timedelta(hours=now.hour) - \
                    datetime.timedelta(minutes=now.minute) - datetime.timedelta(seconds=now.second) - \
                    datetime.timedelta(microseconds=now.microsecond) + datetime.timedelta(hours=12)
        sched = []
        rel_sched = []
        if now < half_day:
            rel_sched = bus_sched[:6]
        else:
            rel_sched = bus_sched[6:]
        for bus in rel_sched:
            next = datetime.datetime.fromtimestamp(time.time()) - datetime.timedelta(hours=now.hour) - \
                    datetime.timedelta(minutes=now.minute) - datetime.timedelta(seconds=now.second) - \
                    datetime.timedelta(microseconds=now.microsecond) + datetime.timedelta(hours=int(bus.split(':')[0])) + \
                    datetime.timedelta(minutes=int(bus.split(':')[1]))
            if now < next:
                sched.append(bus)
        result = ''
        for i in range(sched.__len__()):
            if i == 0:
                result += 'Следующие автобусы: \n<b>' + sched[i] + '</b>\n'
            elif i < 3:
                result += sched[i] + '\n'
            else:
                break
        if sched.__len__() == 0:
            if now < half_day:
                result += 'Сегодня утром автобусов больше не будет'
            else:
                result += 'Сегодня вечером автобусов больше не будет'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Расписание', callback_data='Расписание'))
        markup.add(types.InlineKeyboardButton(text='Остановки', callback_data='Остановки'))
        bot.send_message(message.chat.id, text=result, parse_mode='html', reply_markup=markup)
    except Exception as ex:
        print('Exception of type {!s}: {!s}'.format(type(ex).__name__, str(ex)))
        bot.send_message(message.chat.id, text='Извините, но что-то пошло не так', reply_markup=get_default_markup())
        pass
    return


"""
Отображение вакансий в разбивке по направлениям
"""


def work_hh_category(city):
    spec = get_data('hh_spec', '')
    spec_dict = {}
    #markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup = types.InlineKeyboardMarkup()
    for i in range(spec.__len__()):
        spec_dict[int(spec[i]['id'])] = spec[i]['name']
    area = ''
    if city == 'Саратов':
        area = '&area=79'
    elif city == 'Санкт-Петербург':
        area = '&area=2'
    elif city == 'Москва':
        area = '&area=1'
    for i in range(30):
        feed = get_data('hh', '&specialization=' + str(i + 1) + area)
        if feed['items'].__len__() != 0:
            button = types.InlineKeyboardButton(text=spec_dict[i + 1] + ' (' + str(feed['items'].__len__()) + ')',
                            callback_data='&specialization=' + str(i + 1) + area)
            markup.add(button)
    return markup


