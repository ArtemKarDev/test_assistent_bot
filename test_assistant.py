import wikipedia
from telebot import TeleBot, types
from faker import Faker
import json
import time
from secrets import token_urlsafe

TOKEN_BOT = ''
with open('token.txt','r') as f:
    TOKEN_BOT = f.read()
f.close()

bot = TeleBot(token=TOKEN_BOT, parse_mode='html') # создание бота

faker = Faker() # утилита для генерации номеров кредитных карт
card_systempay = ['Maestro', 'Mastercard', 'VISA', 'JCB']
    #['maestro', 'mastercard', 'visa13', 'visa16', 'visa19', 'amex', 'discover', 'diners', 'jcb15', 'jcb16']



# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Спросить в Wiki")
    btn2 = types.KeyboardButton('JSON валидатор')
    btn3 = types.KeyboardButton("Пользовательские данные")
    btn4 = types.KeyboardButton('Номер Банковской карты')
    btn5 = types.KeyboardButton('КОТЭ1')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Чего сделать?", reply_markup=markup)


# обработчик всех остальных сообщений

@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой либо из кнопок
    if message.text == 'Номер Банковской карты':
        card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("VISA")
        btn2 = types.KeyboardButton('Mastercard')
        btn3 = types.KeyboardButton("Maestro")
        btn4 = types.KeyboardButton('JCB')
        btn5 = types.KeyboardButton("В Главное Меню3")
        card_type_keybaord.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Выбери платёжную систему.", reply_markup=card_type_keybaord)

    elif message.text == 'В Главное Меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Спросить в Wiki")
        btn2 = types.KeyboardButton('JSON валидатор')
        btn3 = types.KeyboardButton("Пользовательские данные")
        btn4 = types.KeyboardButton('Номер Банковской карты')
        btn5 = types.KeyboardButton('КОТЭ')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Чего сделать?", reply_markup=markup)

#
    #  добавить в бота кнопку меню !!!!!!!!!!!! ге моно бцдет выбирать старт
    #
    #  Этот блок с картами надо в отдельную функцию убрать!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
     #

    # в зависимости от типа карты присваем занчение переменной 'card_type'
    elif message.text in  card_systempay:
        if message.text == 'VISA':
            card_type = 'visa'
        elif message.text == 'Mastercard':
            card_type = 'mastercard'
        elif message.text == 'Maestro':
            card_type = 'maestro'
        elif message.text == 'JCB':
            card_type = 'jcb'

        card_number = faker.credit_card_number(card_type)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Тестовая карта {card_type}:\n<code>{card_number}</code>'
        )
        card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        card_type_keybaord.row(
            types.KeyboardButton(text="VISA"),
            types.KeyboardButton(text="Mastercard"),
            types.KeyboardButton(text="Maestro"),
            types.KeyboardButton(text="JCB")
        )
        # второй ряд кнопок
        card_type_keybaord.row(
            types.KeyboardButton(text="В Главное Меню"))

        # btn1 = types.KeyboardButton("VISA")
        # btn2 = types.KeyboardButton('Mastercard')
        # btn3 = types.KeyboardButton("Maestro")
        # btn4 = types.KeyboardButton('JCB')
        # btn5 = types.KeyboardButton("В Главное Меню")
        # card_type_keybaord.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Выбери платёжную систему.", reply_markup=card_type_keybaord)


    elif message.text == 'Пользовательские данные':
        # объект клавиаутры
        main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # первый ряд кнопок
        main_menu_reply_markup.row(
            types.KeyboardButton(text="1️⃣"),
            types.KeyboardButton(text="2️⃣"),
            types.KeyboardButton(text="5️⃣"),
            types.KeyboardButton(text="🔟")
        )
        # второй ряд кнопок
        main_menu_reply_markup.row(
            types.KeyboardButton(text="В Главное Меню")

        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Выбери сколько пользователей тебе нужно 👇🏻",
            reply_markup=main_menu_reply_markup
        )
        bot.register_next_step_handler(message, get_user_data)

    elif message.text == 'Спросить в Wiki':
        bot.send_message(message.chat.id, "Wikipedia слушает...")
        bot.register_next_step_handler(message, ask_Wiki)

    elif message.text == 'JSON валидатор':
        bot.send_message(message.chat.id, "Давай. Что проверить?")
        bot.register_next_step_handler(message, valid_json)

    elif message.text == 'КОТЭ':
        url = f'https://cataas.com/cat?t=${time.time()}'
        bot.send_photo(message.chat.id, url)

    else:
        # если текст не совпал ни с одной из кнопок
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='Не понимаю тебя :(',
        )
        #return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Спросить в Wiki")
        btn2 = types.KeyboardButton('JSON валидатор')
        btn3 = types.KeyboardButton("Пользовательские данные")
        btn4 = types.KeyboardButton('Номер Банковской карты')
        btn5 = types.KeyboardButton('КОТЭ')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Чего сделать?", reply_markup=markup)


def get_user_data(message: types.Message):
    # определяем количество тестовых пользователей
    # или отправляем ошибку
    payload_len = 0
    if message.text == "В Главное Меню":
        bot.register_next_step_handler(message, message_handler)
        return
    elif message.text == "1️⃣":
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
        return

    # генерируем тестовые данные для выбранного количества пользователей
    # при помощи метода simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # сериализуем данные в строку
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )
    # отправляем результат
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.register_next_step_handler(message, message_handler)



def valid_json(message: types.Message):
    if message.text == "В Главное Меню":
        bot.register_next_step_handler(message, message_handler)
        return
    try:
        # пытаемся распарсить JSON из текста сообщения
        payload = json.loads(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Спросить в Wiki")
        btn2 = types.KeyboardButton('JSON валидатор')
        btn3 = types.KeyboardButton("Пользовательские данные")
        btn4 = types.KeyboardButton('Номер Банковской карты')
        btn5 = types.KeyboardButton('КОТЭ')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.register_next_step_handler(message, message_handler, reply_markup=markup)
    except json.JSONDecodeError as ex:
        # при ошибке взникнет исключение 'json.JSONDecodeError'
        # преобразовываем исключение в строку и выводим пользователю
        bot.send_message(
            chat_id=message.chat.id,
            text=f'При обработке произошла ошибка:\n<code>{str(ex)}</code>'
        )
        # выходим из функции
        return

    # если исключения не возникло - значит был введен корректный JSON
    # форматируем его в красивый текст :) (отступ 2 пробела на уровень, сортировать ключи по алфавиту)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'JSON:\n<code>{text}</code>'
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Спросить в Wiki")
    btn2 = types.KeyboardButton('JSON валидатор')
    btn3 = types.KeyboardButton("Пользовательские данные")
    btn4 = types.KeyboardButton('Номер Банковской карты')
    btn5 = types.KeyboardButton('КОТЭ')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.register_next_step_handler(message, message_handler, reply_markup=markup)



def ask_Wiki(message):
    try:
        wikipedia.set_lang("ru")
        bot.send_message(message.from_user.id, wikipedia.summary(str(message.text)))
    except:
        bot.send_message(message.from_user.id, "Такого слова в Wikipedia нет")
        bot.send_message(message.from_user.id, """Можете найти в интернете по ссылке:""" + """https://yandex.ru/search/?text="""
                        + message.text.replace(' ', '+') )

    bot.register_next_step_handler(message, message_handler)
        





# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()