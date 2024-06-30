import logging
import os

import requests
from dotenv import load_dotenv
from telebot import TeleBot, types

from constants import URL_CAT, URL_DOG

load_dotenv()

secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def get_new_image():
    try:
        response = requests.get(URL_CAT)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_DOG)

    response = response.json()
    random_animal = response[0].get('url')
    return random_animal


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat_id = message.chat.id
    bot.send_photo(chat_id, get_new_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('/newcat')
    keyboard.add(button)

    bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашел',
        reply_markup=keyboard,
    )

    bot.send_photo(chat_id, get_new_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
