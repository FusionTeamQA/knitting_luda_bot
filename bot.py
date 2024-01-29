import os
import sys
import time
from datetime import datetime

import gspread
import pytz
import telebot
from oauth2client.service_account import ServiceAccountCredentials
from requests import ReadTimeout
from telebot import types
from telebot.types import ReplyKeyboardRemove
import random


from products import products_bag
from products import products_games
from products import products_baskets

import setting

bot = telebot.TeleBot(setting.token_prod)
# Заказ
user_dict = {}
user_chats = 0

generated_numbers = []

def generate_unique_random_number():
    global generated_numbers
    number = random.randint(0, 500)
    while number in generated_numbers:
        number = random.randint(0, 500)
    generated_numbers.append(number)
    return number
class User:

    def __init__(self, name):
        self.name = None
        self.type = None
        self.for_whom = None
        self.holiday = None
        self.kontakt_numb = None
        self.git_acc1 = None

        keys = ['name', 'type', 'for_whom', 'holiday', 'kontakt_numb', 'git_acc1']

        for key in keys:
            self.key = None


# Предполагается, что у вас есть список продуктов
products_bag = products_bag
current_index = 0  # Начальный индекс для пагинации


dt_string = None  # Установка даты и времени

# Установка параметров доступа к Google API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('key/key.json', scope)
client = gspread.authorize(credentials)

# Открытие таблицы по URL
url = 'https://docs.google.com/spreadsheets/d/1tPyAv6qoarR_bRTPt61ZeMoKI9VNDMV8hyN1EDN6wlc/edit#gid=274948492'
sheet = client.open_by_url(url).sheet1

url_log = 'https://docs.google.com/spreadsheets/d/1tPyAv6qoarR_bRTPt61ZeMoKI9VNDMV8hyN1EDN6wlc/edit#gid=97989579'
sheet_log = client.open_by_url(url_log).worksheet('Log')

url_orders = 'https://docs.google.com/spreadsheets/d/1tPyAv6qoarR_bRTPt61ZeMoKI9VNDMV8hyN1EDN6wlc/edit#gid=1272584257'
sheet_orders = client.open_by_url(url_log).worksheet('Orders')

url_lottery = 'https://docs.google.com/spreadsheets/d/1tPyAv6qoarR_bRTPt61ZeMoKI9VNDMV8hyN1EDN6wlc/edit#gid=1699828975'
sheet_lottery = client.open_by_url(url_log).worksheet('Lottery')


data = sheet.get_all_records()

@bot.message_handler(commands=['start'])
def start(message):
    try:
        target_timezone = pytz.timezone('Europe/Moscow')
        now = datetime.now(tz=target_timezone)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        data_to_insert = [message.text, message.from_user.username, dt_string]
        sheet.append_row(data_to_insert)
        sheet_log.append_row(data_to_insert)
        user_id = message.from_user.id
        channel_id = -1002077580466  # замените на ID вашего канала
        chat_member = bot.get_chat_member(channel_id, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            bot.send_message(message.from_user.id,
                             "Добро пожаловать в нашу группу по изготовлению вязанных игрушек и корзинок! "
                             "У нас вы можете заказать любую вязанную вещь по вашему желанию.")
            bot.send_message(message.from_user.id,
                             "💫 Просто расскажите нам, что вы хотите, и мы с удовольствием сделаем это для вас.")
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton('🎁 Заказать изделие')
            btn2 = types.KeyboardButton('🎉 Розыгрыш')
            btn3 = types.KeyboardButton('🌟 Наши работы')
            btn4 = types.KeyboardButton('☎️ Контакты')
            btn7 = types.KeyboardButton('✨ Акции')
            btn5 = types.KeyboardButton('📝 Подписаться на канал')
            btn6 = types.KeyboardButton('👌 Инструкция по уходу')
            markup.add(btn1, btn2, btn3, btn4, btn7, btn5, btn6)
            bot.send_message(message.from_user.id,
                             "Не стесняйтесь задавать вопросы и делиться своими идеями. Надеемся, вы найдете у нас то, что ищете! 🧶🧸🧺",
                             reply_markup=markup)
        else:
            bot.send_message(user_id, "Для использования бота, пожалуйста, подпишитесь на наше сообщество. https://t.me/MagicCrochet_61", parse_mode='html')
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, "Произошла ошибка при проверке подписки.")


@bot.message_handler(func=lambda message: message.text == '🌟 Наши работы')
def handle_works_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🧺 Корзины и наборы')
    btn3 = types.KeyboardButton('🧸 Игрушки')
    btn4 = types.KeyboardButton('👛 Сумки')
    btn5 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1, btn3, btn4, btn5)
    bot.send_message(message.from_user.id, '⬇ Выберите интересующий раздел', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '✨ Акции')
def handle_action_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('👫 Приведи друга')
    btn3 = types.KeyboardButton('❇️ Скидка на 2-е изделие')
    btn4 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1, btn3, btn4)
    bot.send_message(message.from_user.id, '⬇ Выберите интересующий раздел', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '👫 Приведи друга')
def handle_action_friend(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Перейти и поделиться каналом", url="https://t.me/MagicCrochet_61")
    keyboard.add(url_button)
    bot.send_message(message.from_user.id, 'Приведи друга и получи 50% скидку на свой следующий заказ в студии вязания! Просто приведи друга, который сделает покупку, и оба вы получите по 50% скидки на ваши заказы. '
                                           '🎉 Радуйтесь вместе, делись уютом и радостью рукоделия с друзьями! 🧶✨', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == '❇️ Скидка на 2-е изделие')
def handle_action_discount(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    keyboard = telebot.types.InlineKeyboardMarkup()
    luda_button_tg = telebot.types.InlineKeyboardButton(text="Сделать заказ в Телеграм", url=setting.Luda)
    luda_button_vk = telebot.types.InlineKeyboardButton(text="Сделать заказ в ВКонтакте", url=setting.VK)
    keyboard.add(luda_button_tg, luda_button_vk)
    bot.send_message(message.from_user.id, 'При покупке двух изделий в студии вязания, получи скидку на второе изделие 30%! Наслаждайся уютом и красотой вдвойне с уникальными вязаными персонажами. '
                                           '🎁🧶✨ Удиви себя и своих близких прекрасными подарками ручной работы!' , reply_markup=keyboard)



@bot.message_handler(func=lambda message: message.text == '🎉 Розыгрыш')

def handle_raffle_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🥇 Зарегистрироваться на розыгрыш')
    btn2 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, '🔍При нажатии на кнопку "🥇 Зарегистрироваться на розыгрыш" вы согласны на обработку персональных данных из вашего аккаунта Телеграм.')
    bot.send_message(message.from_user.id, '⬇ Получите свой номерок участника розыгрыша, нажав на кнопку', reply_markup=markup)

last_raffle_time = {}

@bot.message_handler(func=lambda message: message.text == '🥇 Зарегистрироваться на розыгрыш')
def handle_raffle(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_raffle_time:
        time_since_last_raffle = current_time - last_raffle_time[user_id]
        if time_since_last_raffle < 24*60*60:  # Если прошло менее 24 часов
            bot.send_message(user_id, "Вы уже участвовали в розыгрыше за последние 24 часа. Повторно получить номерок можно только через 24 часа")
            return
    last_raffle_time[user_id] = current_time
    random_number = generate_unique_random_number()
    bot.send_message(user_id, f"Поздравляем! Ваш уникальный случайный номер: {random_number}")
    data_to_insert = [message.from_user.username, message.from_user.first_name, message.from_user.last_name, random_number, dt_string]
    sheet_lottery.append_row(data_to_insert)

# Отправка Сумок
@bot.message_handler(func=lambda message: message.text == '👛 Сумки')
def handle_bags_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    global current_index
    current_index = 0  # Сброс пагинации
    send_batch(message)


def send_batch(message):
    global current_index
    batch_size = 2  # Количество продуктов для показа
    end_index = current_index + batch_size

    # Отправка продуктов в текущей "порции"
    for product in products_bag[current_index:end_index]:
        with open(product['image_path'], 'rb') as photo:
            # Отправка информации о продукте, например, фото
            bot.send_photo(message.chat.id, photo, caption=f"<b>{product['name']}</b>\n\n{product['description']}",
                           parse_mode="HTML")
    # Обновление индекса для следующей "порции"
    current_index = end_index

    # Если продукты ещё остались, показываем кнопку "Показать ещё"
    if current_index < len(products_bag):
        markup = telebot.types.InlineKeyboardMarkup()
        load_more_button = telebot.types.InlineKeyboardButton(text='Показать ещё 🤩', callback_data='load_more')
        markup.add(load_more_button)
        remaining_products = len(products_bag) - current_index
        if remaining_products == 1:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работа, показать? 🙈',
                             reply_markup=markup)
        elif remaining_products < 5:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работы, показать? 🙈',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работ, показать? 🙈',
                             reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'load_more')
def handle_load_more(call):
    send_batch(call.message)
    bot.answer_callback_query(call.id)


# Отправка Игрушек
@bot.message_handler(func=lambda message: message.text == '🧸 Игрушки')
def handle_games_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    global current_index
    current_index = 0  # Сброс пагинации
    send_batch_games(message)


def send_batch_games(message):
    global current_index
    batch_size = 2  # Количество продуктов для показа
    end_index = current_index + batch_size

    # Отправка продуктов в текущей "порции"
    for product in products_games[current_index:end_index]:
        with open(product['image_path'], 'rb') as photo:
            # Отправка информации о продукте, например, фото
            bot.send_photo(message.chat.id, photo, caption=f"<b>{product['name']}</b>\n\n{product['description']}",
                           parse_mode="HTML")
    # Обновление индекса для следующей "порции"
    current_index = end_index

    # Если продукты ещё остались, показываем кнопку "Показать ещё"
    if current_index < len(products_games):
        markup = telebot.types.InlineKeyboardMarkup()
        load_more_button = telebot.types.InlineKeyboardButton(text='Показать ещё 🤩', callback_data='load_more_games')
        markup.add(load_more_button)
        remaining_products = len(products_games) - current_index
        if remaining_products == 1:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работа, показать? 🙈',
                             reply_markup=markup)
        elif remaining_products < 5:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работы, показать? 🙈',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работ, показать? 🙈',
                             reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'load_more_games')
def handle_load_more(call):
    send_batch_games(call.message)
    bot.answer_callback_query(call.id)


# Отправка Корзинок
@bot.message_handler(func=lambda message: message.text == '🧺 Корзины и наборы')
def handle_basket_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    bot.send_message(message.from_user.id,
                     'Стильные корзинки сделают Ваш дом уютным и модным. Отличная идея для подарка.\n')
    global current_index
    current_index = 0  # Сброс пагинации
    send_batch_basket(message)


def send_batch_basket(message):
    global current_index
    batch_size = 2  # Количество продуктов для показа
    end_index = current_index + batch_size

    # Отправка продуктов в текущей "порции"
    for product in products_baskets[current_index:end_index]:
        with open(product['image_path'], 'rb') as photo:
            # Отправка информации о продукте, например, фото
            bot.send_photo(message.chat.id, photo, caption=f"<b>{product['name']}</b>\n\n{product['description']}",
                           parse_mode="HTML")
    # Обновление индекса для следующей "порции"
    current_index = end_index

    # Если продукты ещё остались, показываем кнопку "Показать ещё"
    if current_index < len(products_baskets):
        markup = telebot.types.InlineKeyboardMarkup()
        load_more_button = telebot.types.InlineKeyboardButton(text='Показать ещё 🤩', callback_data='load_more_basket')
        markup.add(load_more_button)
        remaining_products = len(products_baskets) - current_index
        if remaining_products == 1:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работа, показать? 🙈',
                             reply_markup=markup)
        elif remaining_products < 5:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работы, показать? 🙈',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Найдены еще ' + str(remaining_products) + ' работ, показать? 🙈',
                             reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'load_more_basket')
def handle_load_more(call):
    send_batch_basket(call.message)
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: message.text == '🔙 Главное меню')
def handle_menu_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🎁 Заказать изделие')
    btn2 = types.KeyboardButton('🎉 Розыгрыш')
    btn3 = types.KeyboardButton('🌟 Наши работы')
    btn4 = types.KeyboardButton('☎️ Контакты')
    btn7 = types.KeyboardButton('✨ Акции')
    btn5 = types.KeyboardButton('📝 Подписаться на канал')
    btn6 = types.KeyboardButton('👌 Инструкция по уходу')
    markup.add(btn1, btn2, btn3, btn4, btn7, btn5, btn6)
    bot.send_message(message.from_user.id, '⬇ Выберите нужный раздел', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '☎️ Контакты')
def handle_contacts_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1)
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Связаться с нами в Telegram", url="https://t.me/@Lyudo4ek_1986")
    keyboard.add(button)
    bot.send_message(message.from_user.id, 'Написать Вконтакте: \n' + setting.VK, disable_web_page_preview=True,
                     reply_markup=markup)
    bot.send_contact(message.from_user.id, '+79888904608', 'Людмила', 'Байгузина', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '📝 Подписаться на канал')
def handle_subscribe_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/MagicCrochet_61")
    keyboard.add(button)
    bot.send_message(chat_id=message.chat.id, text="Нажмите кнопку чтобы перейти и подписаться на канал:",
                     reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == '👌 Инструкция по уходу')
def handle_instruction_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    with open('instruction.txt', 'r') as file:
        instr_text = file.read()
    bot.send_message(chat_id=message.chat.id, text=instr_text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🎁 Заказать изделие')
    btn5 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1, btn5)
    bot.send_message(chat_id=message.chat.id, text="Закажите изделие ручной работы уже сейчас! 🤩💃", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🎁 Заказать изделие')
def handle_order_command(message):
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert = [message.text, message.from_user.username, dt_string]
    sheet_log.append_row(data_to_insert)
    chat_id = message.chat.id
    board = types.InlineKeyboardMarkup()
    cancel = types.InlineKeyboardButton(text="🙅 Отменить заявку", callback_data="Отмена")
    board.add(cancel)
    msg = bot.send_message(chat_id, "Добрый день, представьтесь пожалуйста.", reply_markup=board)
    bot.register_next_step_handler(msg, name_step)


def name_step(message, user=None):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="🙅 Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        user.name = name
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🧺 Корзины и наборы')
        btn3 = types.KeyboardButton('🧸 Игрушки')
        btn4 = types.KeyboardButton('👛 Сумки')
        markup.add(btn1, btn3, btn4)
        msg = bot.send_message(chat_id, "Какой вид изделия вас интересует", reply_markup=markup)
        bot.register_next_step_handler(msg, process_type)
    except Exception as e:
        bot.reply_to(message, 'Ошибка, попробуйте позже')
    # keys = ['name', 'type', 'for_whom', 'holiday', 'kontakt_numb', 'git_acc1']


def process_type(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="🙅 Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        type = message.text
        user = user_dict[chat_id]
        user.type = type
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        msg = bot.send_message(chat_id, 'Для кого будет выполнено изделие?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_for_whom)
    except Exception as e:
        bot.reply_to(message, 'Ошибка, попробуйте позже')


def process_for_whom(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="🙅 Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        for_whom = message.text
        user = user_dict[chat_id]
        user.for_whom = for_whom
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        msg = bot.send_message(chat_id, 'Под какой праздник планируется изделие?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_kontact)
    except Exception as e:
        bot.reply_to(message, 'Ошибка, попробуйте позже')


def process_kontact(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="🙅 Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        holiday = message.text
        user = user_dict[chat_id]
        user.holiday = holiday
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        msg = bot.send_message(chat_id, 'Укажите номер телефона, для связи с вами', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_dop_kom)
    except Exception as e:
        bot.reply_to(message, 'Ошибка, попробуйте позже')


def process_dop_kom(message):
    try:
        board = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text="🙅 Отменить заявку", callback_data="Отмена")
        board.add(cancel)
        chat_id = message.chat.id
        kontakt_numb = message.text
        user = user_dict[chat_id]
        user.kontakt_numb = kontakt_numb
        if not kontakt_numb.isdigit() or len(kontakt_numb) != 11:
            msg = bot.send_message(chat_id, 'Номер должен состоять из 11 цифр. Пожалуйста, введите корректный номер.')
            bot.register_next_step_handler(msg, process_dop_kom)
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔄Пропустить шаг')
        markup.add(btn1)
        msg = bot.send_message(chat_id, 'Дополнительные пожелания к изделию', reply_markup=markup)
        bot.register_next_step_handler(msg, send_z)
    except Exception as e:
        bot.reply_to(message, 'Ошибка, попробуйте позже')


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
    bot.send_message(setting.admin_id_ugraswim,
                     f'Поступила новая заявка на изделие от {app_name_first[0]} {app_name_last[0]} !\n'
                     + f'username в тг = @{app_username[0]} \n'
                     + f'Имя  -  {user.name} \n'
                     + f'Тип  -  {user.type} \n'
                     + f'Для кого  -  {user.for_whom} \n'
                     + f'Праздник  -  {user.holiday} \n'
                     + f'Контактные данные: {user.kontakt_numb} \n'
                     + f'Дополнительные комментарии: {app_text[0]} \n'

                     + f'ID юзера: {user_chats}')
    bot.send_message(setting.group_id_manager,
                     f'Поступила новая заявка на изделие от {app_name_first[0]} {app_name_last[0]} !\n'
                     + f'username в тг = @{app_username[0]} \n'
                     + f'Имя  -  {user.name} \n'
                     + f'Тип  -  {user.type} \n'
                     + f'Для кого  -  {user.for_whom} \n'
                     + f'Праздник  -  {user.holiday} \n'
                     + f'Контактные данные: {user.kontakt_numb} \n'
                     + f'Дополнительные комментарии: {app_text[0]} \n'

                     + f'ID юзера: {user_chats}')
    target_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=target_timezone)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_to_insert_orders = [user.name, user.type, user.for_whom, user.holiday, user.kontakt_numb, app_text[0], message.from_user.username, dt_string]
    sheet_orders.append_row(data_to_insert_orders)
    app_name_first.clear()
    app_name_last.clear()
    app_username.clear()
    app_text.clear()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn1)
    bot.send_message(chat_id, "Заявка отправлена, мы свяжемся с Вами в ближайшее время", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    chat_id = call.message.chat.id
    if call.message:
        if call.data == "Отмена":
            target_timezone = pytz.timezone('Europe/Moscow')
            now = datetime.now(tz=target_timezone)
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            data_to_insert = ['Отмена заявки', call.message.chat.username, dt_string]
            sheet_log.append_row(data_to_insert)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton('🎁 Заказать изделие')
            btn3 = types.KeyboardButton('🌟 Наши работы')
            btn4 = types.KeyboardButton('☎️ Контакты')
            btn5 = types.KeyboardButton('📝 Подписаться на канал')
            btn6 = types.KeyboardButton('👌 Инструкция по уходу')
            markup.add(btn1, btn3, btn4, btn5, btn6)
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Отмена заполнения заявки...')
            bot.send_message(chat_id=call.message.chat.id, text='⬇ Выберите нужный раздел', reply_markup=markup)
            bot.clear_step_handler(msg)


try:
    bot.infinity_polling(timeout=90, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=90, long_polling_timeout=5)
