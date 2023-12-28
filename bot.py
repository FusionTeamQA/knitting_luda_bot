# -*- coding: utf-8 -*-
import time

from requests import ReadTimeout
from telebot.types import ReplyKeyboardRemove
import requests
import telebot
from datetime import datetime
from telebot import types
import setting
import os, sys
import sqlite3
import pytz


bot = telebot.TeleBot(setting.token_test)
user_dict = {}
user_chats = 0
dt_string = None  # Установка даты и времени


class User:

    def __init__(self, name):
        self.name = None
        self.object_kond = None
        self.visota_potilka = None
        self.ploshad = None
        self.trassa = None
        self.orientation = None
        self.people_kol_vo = None
        self.people_charakter_work = None
        self.sum_all_teplo_raschet = None
        self.sum_all_teplo_trebuemaya_proizvod = None
        self.dop_kontr_ispol = None
        self.dop_hlodagent = None
        self.dop_modification = None
        self.zamer_online = None
        self.kontakt_numb = None
        self.git_acc1 = None

        self.object = None
        self.ploshad_object = None
        self.visota_object = None
        self.task_system = None
        self.project = None
        self.plan = None
        self.model_oborud = None
        self.stage_object = None
        self.city = None
        self.number = None

        keys = ['name', 'object_kond', 'visota_potilka', 'ploshad', 'trassa', 'orientation', 'people_kol_vo',
                'people_charakter_work', 'sum_all_teplo_raschet', 'sum_all_teplo_trebuemaya_proizvod',
                'dop_kontr_ispol', 'dop_hlodagent', 'zamer_online', 'dop_modification', 'kontakt_numb', 'nums',
                'git_acc1',
                'object', 'ploshad_object', 'visota_object', 'task_system',
                'project', 'plan', 'model_oborud', 'stage_object', 'city', 'number']

        for key in keys:
            self.key = None

user_state = {}

@bot.message_handler(commands=['start'])  # стартовая команда
def start(message):
    conn = sqlite3.connect('database_users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER, 
            user_first_name TEXT, 
            user_last_name TEXT, 
            username TEXT,
            data_time varchar(50)
            )''')
    conn.commit()
    people_id = message.from_user.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        target_timezone = pytz.timezone('Europe/Moscow')
        now = datetime.now(tz=target_timezone)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        USER_ID = [message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                   message.from_user.username, dt_string]
        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?);", USER_ID)
        conn.commit()
        conn.close()
    else:
        print(message.from_user.username)
        print(message.from_user.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🎁 Заказать изделие')
    btn3 = types.KeyboardButton('🌟 Наши работы')
    btn4 = types.KeyboardButton('☎️ Контакты')
    btn5 = types.KeyboardButton('📝 Подписаться на канал')
    markup.add(btn1, btn3, btn4, btn5)
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    bot.send_message(message.from_user.id, "Добро пожаловать в нашу группу по продаже вязанных игрушек и корзинок! "
                                           "У нас вы можете заказать любую вязанную вещь по вашему желанию.", reply_markup=markup)
    bot.send_message(message.from_user.id, "💫 Просто расскажите нам, что вы хотите, и мы с удовольствием сделаем это для вас.")
    bot.send_message(message.from_user.id,"Не стесняйтесь задавать вопросы и делиться своими идеями. Надеемся, вы найдете у нас то, что ищете! 🧶🧸🧺", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '🔙 Главное меню':
        target_timezone = pytz.timezone('Europe/Moscow')
        now = datetime.now(tz=target_timezone)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('🎁 Заказать изделие')
        btn3 = types.KeyboardButton('🌟 Наши работы')
        btn4 = types.KeyboardButton('☎️ Контакты')
        btn5 = types.KeyboardButton('📝 Подписаться на канал')
        markup.add(btn1, btn3, btn4, btn5)
        bot.send_message(message.from_user.id, '⬇ Выберите нужный раздел', reply_markup=markup)


    elif message.text == '☎️ Контакты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn1)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Связаться с нами в Telegram", url="https://t.me/@Lyudo4ek_1986")
        keyboard.add(button)
        bot.send_message(message.from_user.id, 'Написать Вконтакте: \n' + setting.VK, disable_web_page_preview=True, reply_markup=markup)
        bot.send_contact(message.from_user.id, '+79888904608', 'Людмила',  'Байгузина', reply_markup=keyboard)


    elif message.text == '📝 Подписаться на канал':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/MagicCrochet_61")
        keyboard.add(button)
        bot.send_message(chat_id=message.chat.id, text="Нажмите кнопку, чтобы подписаться на канал:",
                         reply_markup=keyboard)

    elif message.text == '🌟 Наши работы':
        target_timezone = pytz.timezone('Europe/Moscow')
        now = datetime.now(tz=target_timezone)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🧺 Корзины и наборы')
        btn3 = types.KeyboardButton('🧸 Игрушки')
        btn4 = types.KeyboardButton('👛 Сумки')
        btn5 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn1, btn3, btn4, btn5)
        bot.send_message(message.from_user.id, '⬇ Выберите интересующий раздел', reply_markup=markup)

    elif message.text == '🧺 Корзины и наборы':
        bot.send_message(message.from_user.id, 'Стильные корзинки сделают Ваш дом уютным и модным. Отличная идея для подарка.\n')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn5 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn5)
        bot.send_photo(message.from_user.id, open('img/1.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: полиэфирный шнур, держит форму, деревянное донышко. \n'
                                               'Размеры корзины: 18 см диаметр донышка, 11 см высота корзинки.\n'
                                               'Цена 500 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(3)
        bot.send_photo(message.from_user.id, open('img/2.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: трикотажная пряжа (100% хлопок), держит форму, деревянное донышко.\n'
                                               'Размеры корзины: 20 см диаметр донышка, 12 см высота корзинки.\n'
                                               'Цена 700 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(3)
        bot.send_photo(message.from_user.id, open('img/3.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: трикотажная пряжа (100% хлопок), держит форму, деревянное донышко.\n'
                         'Размеры корзины: 12 см диаметр донышка, 8 см высота корзинки.\n'
                         'Цена 350 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(3)
        bot.send_photo(message.from_user.id, open('img/4.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: трикотажная пряжа (100% хлопок), держит форму, деревянное донышко.\n'
                         'Размеры корзины: 18, 13, 8 см диаметры донышек, 11 см высота корзинки.\n'
                         'Цена 1200 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('img/5.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: трикотажная пряжа (100% хлопок), держит форму, деревянное донышко.\n'
                         'Размеры корзины: 20, 16, 11 см диаметры донышек, 9 см высота корзинки.\n'
                         'Цена 1200 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('img/6.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: трикотажная пряжа (100% хлопок), держит форму, деревянное донышко.\n'
                         'Размеры корзины: 18, 13, 8 см диаметры донышек, 10 см высота корзинки.\n'
                         'Цена 1200 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('img/7.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: трикотажная пряжа (100% хлопок), держит форму, деревянное донышко.\n'
                         'Размеры корзины: 18, 13, см диаметры донышек, 11 см высота корзинки.  \n'
                         'Цена 850 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('img/8.jpg', 'rb'))
        bot.send_message(message.from_user.id, 'Материал: трикотажная пряжа (100% хлопок), держит форму, деревянное донышко.\n'
                         'Размеры корзины: 18, 8, 8 см диаметры донышек, 11 см высота корзинки.\n'
                         'Цена 1200 рублей.\nСрок изготовления: 7 дней', reply_markup=markup)
        time.sleep(2)


    elif message.text == '🧸 Игрушки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn5 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn5)
        bot.send_message(message.from_user.id, 'Вязанная игрушка крючком станет отличным подарком для ребенка любого возраста.', reply_markup=markup)

        products = [
            {
                'name': 'Щелкунчик',
                'description': 'Связан из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 25 см.\n'
                               'Цена 1000 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/1.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком 30 см',
                'description': 'Связан из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 30 см.\n'
                               'Цена 2500 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/2.jpg'
            },
            {
                'name': 'Снеговик',
                'description': 'Связан из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 20 см.\n'
                               'Цена 800 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/3.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком 35 см',
                'description': 'Связан из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 35 см.\n'
                               'Цена 1500 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/4.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком 35 см',
                'description': 'Связан из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 35 см.\n'
                               'Цена 1600 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/5.jpg'
            },
            {
                'name': 'Чебурашка',
                'description': 'Связан из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 25 см.\n'
                               'Цена 800 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/6.jpg'
            },
            {
                'name': 'Милые медвежата',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 25 см.\n'
                               'Цена 1000 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/7.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком 20 см',
                'description': 'Связана из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 20 см.\n'
                               'Цена 800 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/8.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком 20 см',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 20 см.\n'
                               'Цена 400 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/9.jpg'
            },
            {
                'name': 'Милые совушки',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Цена маленькой совы 300 рублей, большая 700 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/10.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком 30 см',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 30 см.\n'
                               'Цена 700 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/11.jpg'
            },
            {
                'name': 'Голубые береты',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 30 см.\n'
                               'Цена 1500 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/12.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком 30 см',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 30 см.\n'
                               'Цена 1000 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/13.jpg'
            },
            {
                'name': 'Синий трактор',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Высота 25 см.\n'
                               'Цена 1000 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/14.jpg'
            },
            {
                'name': 'Вязанная игрушка крючком',
                'description': 'Связаны из детской пряжи, гипоаллергенный наполнитель. \n'
                               'Все детальки надёжно пришиты.\n'
                               'Цена 500 рублей.\n'
                               'Срок изготовления - 7 дней.',
                'image_path': 'img/games/15.jpg'
            },
        ]
        for product in products:
            with open(product['image_path'], 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=f"<b>{product['name']}</b>\n\n{product['description']}",
                               parse_mode="HTML")
                time.sleep(0.5)

    # Small talk

    elif message.text == 'Привет!':
        bot.send_message(message.from_user.id, 'Привет!')

    elif message.text == 'как дела?':
        bot.send_message(message.from_user.id, 'Хорошо!')

    elif message.text == 'пока':
        bot.send_message(message.from_user.id, 'Всего доброго, заходите еще')

    elif message.text == 'Пока':
        bot.send_message(message.from_user.id, 'Всего доброго, заходите еще')


    elif message.text == '🧮 Заказать изделие':
        chat_id = message.chat.id
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="👈Назад", callback_data="Отмена")
        board.add(cancel)
        msg = bot.send_message(chat_id, "Добрый день, представьтесь пожалуйста.", reply_markup=board)
        bot.register_next_step_handler(msg, name_step)


# '🧮 Заказать изделие
def name_step(message, user=None):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        user.name = name
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Москва')
        btn2 = types.KeyboardButton('Московская область')
        btn3 = types.KeyboardButton('Другое')
        markup.add(btn1, btn2, btn3)
        msg = bot.send_message(chat_id, "Укажите город", reply_markup=markup)
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите "Отменить заявку"', reply_markup=board)
        bot.register_next_step_handler(msg, process_object_kond)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_param_pomeshenia_ploshad(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        ploshad = message.text
        user = user_dict[chat_id]
        user.ploshad = ploshad
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        msg = bot.send_message(chat_id, 'Укажите площадь, в м2', reply_markup=markup)
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        bot.register_next_step_handler(msg, process_param_pomeshenia_visota_potilka)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_object_kond(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        object_kond = message.text
        user = user_dict[chat_id]
        user.object_kond = object_kond
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Квартира')
        btn2 = types.KeyboardButton('Частный дом')
        btn3 = types.KeyboardButton('Офис (Коммерческое помещение)')
        markup.add(btn1, btn2, btn3)
        msg = bot.send_message(chat_id, 'На каком обьекте планируется установка кондиционера?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_param_pomeshenia_ploshad)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_param_pomeshenia_visota_potilka(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        visota_potilka = message.text
        user = user_dict[chat_id]
        user.visota_potilka = visota_potilka
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('До 2.7 метров')
        btn2 = types.KeyboardButton('От 2.7 до 3 метров')
        btn3 = types.KeyboardButton('Более 3 метров')
        btn4 = types.KeyboardButton('Не помню')
        markup.add(btn1, btn2, btn3, btn4)
        msg = bot.send_message(chat_id, 'Укажите высоту потолка, в м', reply_markup=markup)
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        bot.register_next_step_handler(msg, process_trassa)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_trassa(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        trassa = message.text
        user = user_dict[chat_id]
        user.trassa = trassa
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Да')
        btn2 = types.KeyboardButton('Нет')
        btn3 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1, btn2, btn3)
        msg = bot.send_message(chat_id, 'У вас ремонт и требуется прокладка трассы?', reply_markup=markup)
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        bot.register_next_step_handler(msg, process_orientation)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_orientation(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        orientation = message.text
        user = user_dict[chat_id]
        user.orientation = orientation
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('В помещении почти не бывает солнца')
        btn2 = types.KeyboardButton('Среднее значение')
        btn3 = types.KeyboardButton('Большое остекление с солнечной стороны')
        btn4 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1, btn2, btn3, btn4)
        msg = bot.send_message(chat_id, '2. Ориентация окон помещения', reply_markup=markup)
        bot.send_message(chat_id, 'Укажите свой вариант')
        bot.register_next_step_handler(msg, process_people_kol_vo)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_people_kol_vo(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        people_kol_vo = message.text
        user = user_dict[chat_id]
        user.people_kol_vo = people_kol_vo
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        bot.send_message(chat_id, '3. Люди')
        msg = bot.send_message(chat_id, 'Количество человек',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_people_charakter_work)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_people_charakter_work(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        people_charakter_work = message.text
        user = user_dict[chat_id]
        user.people_charakter_work = people_charakter_work
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Отдых')
        btn2 = types.KeyboardButton('Работа в офисе')
        btn3 = types.KeyboardButton('Физический труд')
        btn4 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1, btn2, btn3, btn4)
        msg = bot.send_message(chat_id, 'Характер работы:', reply_markup=markup)
        bot.send_message(chat_id, 'Укажите свой вариант:')
        bot.register_next_step_handler(msg, process_sum_all_teplo_trebuemaya_proizvod)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_sum_all_teplo_raschet(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        sum_all_teplo_raschet = message.text
        user = user_dict[chat_id]
        user.sum_all_teplo_raschet = sum_all_teplo_raschet
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('1-3 кВт')
        btn2 = types.KeyboardButton('3-6 кВт')
        btn3 = types.KeyboardButton('6-9 кВт')
        btn4 = types.KeyboardButton('Более 9 кВт')
        btn5 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(chat_id, '4. Сумма всех теплопритоков')
        msg = bot.send_message(chat_id, 'Расчетные теплопоступления, Вт',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_sum_all_teplo_trebuemaya_proizvod)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_sum_all_teplo_trebuemaya_proizvod(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        sum_all_teplo_trebuemaya_proizvod = message.text
        user = user_dict[chat_id]
        user.sum_all_teplo_trebuemaya_proizvod = sum_all_teplo_trebuemaya_proizvod
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('2 кВт (М 7)')
        btn2 = types.KeyboardButton('2,5 кВт (М 9)')
        btn3 = types.KeyboardButton('3,5 кВт (М 12)')
        btn4 = types.KeyboardButton('5 кВт (М 18)')
        btn5 = types.KeyboardButton('7 кВт (М 24')
        btn6 = types.KeyboardButton('8,5 кВт (М 30)')
        btn7 = types.KeyboardButton('10,5 кВт (М 36)')
        btn8 = types.KeyboardButton('14 кВт (М 42)')
        btn9 = types.KeyboardButton('16 кВт (М60)')
        btn10 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
        msg = bot.send_message(chat_id, 'Требуемая производительность, Вт', reply_markup=markup)
        bot.register_next_step_handler(msg, process_dop_kontr_ispol)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_dop_kontr_ispol(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        dop_kontr_ispol = message.text
        user = user_dict[chat_id]
        user.dop_kontr_ispol = dop_kontr_ispol
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn2 = types.KeyboardButton('Настенный')
        btn3 = types.KeyboardButton('Канальный')
        btn4 = types.KeyboardButton('Напольный')
        btn5 = types.KeyboardButton('Касетный')
        btn6 = types.KeyboardButton('Подвесной')
        btn7 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn2, btn3, btn4, btn5, btn6, btn7)
        msg = bot.send_message(chat_id, 'ДОПОЛНИТЕЛЬНЫЕ СВЕДЕНИЯ', reply_markup=markup)
        bot.send_message(chat_id, 'Конструктивное исполнение:')
        bot.register_next_step_handler(msg, process_dop_modification)

    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_dop_hlodagent(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        dop_hlodagent = message.text
        user = user_dict[chat_id]
        user.dop_hlodagent = dop_hlodagent
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Найти все')
        btn2 = types.KeyboardButton('R22')
        btn3 = types.KeyboardButton('R407C')
        btn4 = types.KeyboardButton('R410A')
        btn5 = types.KeyboardButton('R32')
        btn6 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        msg = bot.send_message(chat_id, 'ДОПОЛНИТЕЛЬНЫЕ СВЕДЕНИЯ', reply_markup=markup)
        bot.send_message(chat_id, 'Хладагент:')
        bot.register_next_step_handler(msg, process_dop_modification)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_dop_modification(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        dop_modification = message.text
        user = user_dict[chat_id]
        user.dop_modification = dop_modification
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Найти все')
        btn2 = types.KeyboardButton('Только охлаждение')
        btn3 = types.KeyboardButton('Охлаждение и обогрев')
        markup.add(btn1, btn2, btn3)
        msg = bot.send_message(chat_id, 'ДОПОЛНИТЕЛЬНЫЕ СВЕДЕНИЯ', reply_markup=markup)
        bot.send_message(chat_id, 'Модификация:')
        bot.register_next_step_handler(msg, step_zamer_online)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def step_zamer_online(message):
    try:
        chat_id = message.chat.id
        zamer_online = message.text
        user = user_dict[chat_id]
        user.zamer_online = zamer_online
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Да')
        btn2 = types.KeyboardButton('Нет')
        btn3 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1, btn2, btn3)
        msg = bot.send_message(chat_id, "Нужен ли вам замерщик?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_git_acc_step)

    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_git_acc_step(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="👈Вернуться", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        bot.send_message(message.from_user.id, 'Осталось совсем немного!\n'
                                               'Если вы передумали и хотите вернуться назад, нажмите кнопку "Вернуться в меню".',
                         reply_markup=board)
        git_acc1 = message.text
        user = user_dict[chat_id]
        user.git_acc = git_acc1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        msg = bot.send_message(chat_id, "Контактные данные", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_comment)

    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def process_comment(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        # bot.send_message(message.from_user.id, 'Для отмены заявки нажмите кнопку "Отменить заявку"', reply_markup=board)
        nums = message.text
        user = user_dict[chat_id]
        user.nums = nums
        if not nums.isdigit() or len(nums) != 11:
            msg = bot.send_message(chat_id, 'Номер должен состоять из 11 цифр. Пожалуйста, введите корректный номер.')
            bot.register_next_step_handler(msg, process_comment)
            return
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        msg = bot.send_message(chat_id, "Дополнительный комментарий", reply_markup=markup)
        bot.register_next_step_handler(msg, send_z)
    except Exception as e:
        bot.reply_to(message, 'Непредвиденная ошибка')


def send_z(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    user_name = message.chat.username
    z = message.text  # text user
    app_text = []
    app_name_first = []
    app_name_last = []
    app_username = []
    app_name_first.append(first_name)
    app_name_last.append(last_name)
    app_username.append(user_name)
    app_text.append(z)
    user = user_dict[chat_id]
    user_chats = message.from_user.id
    data_to_insert_kond = [user.name, user.object_kond, user.ploshad, user.trassa, user.orientation,
                           user.visota_potilka, user.people_kol_vo, user.people_charakter_work,
                           user.sum_all_teplo_trebuemaya_proizvod, user.dop_kontr_ispol, user.dop_modification,
                           user.zamer_online, user.git_acc, user.nums, app_text[0], message.from_user.username,
                           dt_string]
    bot.send_message(setting.admin_id_ugraswim,
                     f'Поступила новая заявка по квизу "Кондиционеры" от {app_name_first[0]} {app_name_last[0]} !\n'
                     + f'username в тг = @{app_username[0]} \n'
                     + f'Имя  -  {user.name} \n'
                     + f'Город  -  {user.object_kond} \n'
                     + f'Объект  -  {user.ploshad} \n'
                     + f'Высота потолка  -  {user.trassa} \n'
                     + f'Нужна ли прокладка трассы?: - {user.orientation} \n'
                     + f'Площадь: {user.visota_potilka} \n'
                     + f'Ориентация окон помещения: - {user.people_kol_vo} \n'
                     + f'Количество людей:  -  {user.people_charakter_work} \n'
                     + f'Характер работы  -  {user.sum_all_teplo_trebuemaya_proizvod} \n'
                     + f'Требуемая производительность  -  {user.dop_kontr_ispol} \n'
                     + f'Конструктивное исполнение  -  {user.dop_modification} \n'
                     + f'Модификация  -  {user.zamer_online} \n'
                     + f'Нужен ли замерщик  -  {user.git_acc} \n'
                     + f'Контактные данные: {user.nums} \n'
                     + f'Дополнительные комментарии: {app_text[0]} \n'

                     + f'ID юзера: {user_chats}')

    bot.send_message(setting.group_id_manager,
                     f'Поступила новая заявка по квизу "Кондиционеры" от {app_name_first[0]} {app_name_last[0]} !\n'
                     + f'username в тг = @{app_username[0]} \n'
                     + f'Имя  -  {user.name} \n'
                     + f'Город  -  {user.object_kond} \n'
                     + f'Объект  -  {user.ploshad} \n'
                     + f'Высота потолка  -  {user.trassa} \n'
                     + f'Нужна ли прокладка трассы?: - {user.orientation} \n'
                     + f'Площадь: {user.visota_potilka} \n'
                     + f'Ориентация окон помещения: - {user.people_kol_vo} \n'
                     + f'Количество людей:  -  {user.people_charakter_work} \n'
                     + f'Характер работы  -  {user.sum_all_teplo_trebuemaya_proizvod} \n'
                     + f'Требуемая производительность  -  {user.dop_kontr_ispol} \n'
                     + f'Конструктивное исполнение  -  {user.dop_modification} \n'
                     + f'Модификация  -  {user.zamer_online} \n'
                     + f'Нужен ли замерщик  -  {user.git_acc} \n'
                     + f'Контактные данные: {user.nums} \n'
                     + f'Дополнительные комментарии: {app_text[0]} \n'

                     + f'ID юзера: {user_chats}')

    app_name_first.clear()
    app_name_last.clear()
    app_username.clear()
    app_text.clear()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1)
    bot.send_message(chat_id, "Заявка отправлена, мы свяжемся с Вами в ближайшее время", reply_markup=markup)



@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id

    # Сохраняем фото
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path

    # Пересылаем фото в другой чат или канал
    bot.send_message(setting.group_id_manager,
                     "Поступило новое фото от пользователя: " + str(
                         "@" + message.chat.username + " - " + message.chat.first_name + " " + message.chat.last_name), )
    bot.forward_message(setting.group_id_manager, chat_id, message_id=message.message_id)

    # Отправляем подтверждающее сообщение
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1)
    bot.send_message(chat_id, "Изображение успешно отправлено. Спасибо!", reply_markup=markup)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id

    # Сохраняем файл
    file_info = bot.get_file(message.document.file_id)
    file_path = file_info.file_path

    # Пересылаем файл в другой чат или канал
    bot.send_message(setting.group_id_manager,
                     "Поступил новый файл от пользователя: " + str(
                         "@" + message.chat.username + " - " + message.chat.first_name + " " + message.chat.last_name), )
    bot.forward_message(setting.group_id_manager, chat_id, message_id=message.message_id)
    # Отправляем подтверждающее сообщение
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1)
    bot.send_message(chat_id, "Файл успешно отправлен. Спасибо!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    chat_id = call.message.chat.id

    # Обработка нажатия на кнопку "Отправить фото"
    if call.data == "send_photo":
        # Отправляем сообщение для выбора фото
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn1)
        bot.send_message(chat_id, "Пожалуйста, нажмите на 📎 чтобы загрузить изображение плана/проекта",
                         reply_markup=markup)

    # Обработка нажатия на кнопку "Отправить файл"
    elif call.data == "send_file":
        # Отправляем сообщение для выбора файла
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn1)
        bot.send_message(chat_id, "Пожалуйста, нажмите на 📎 чтобы загрузить файл плана/проекта", reply_markup=markup)

    elif call.message:
        if call.data == "Отмена":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton('🧮 Расчёт кондиционера')
            btn2 = types.KeyboardButton('🧮 Расчёт вентиляции')
            btn3 = types.KeyboardButton('🌐 Сайт')
            btn4 = types.KeyboardButton('☎️ Контакты')
            btn5 = types.KeyboardButton('📝 Подписаться на канал')
            markup.add(btn1, btn2, btn3, btn4, btn5)
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Отмена заполнения заявки...')
            bot.send_message(chat_id=call.message.chat.id, text='Выберите нужный раздел:', reply_markup=markup)

            bot.clear_step_handler(msg)
            target_timezone = pytz.timezone('Europe/Moscow')
            now = datetime.now(tz=target_timezone)
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            data_to_insert = ['Отмена заявки', call.message.chat.username, dt_string]


try:
    bot.infinity_polling(timeout=90, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=90, long_polling_timeout=5)
