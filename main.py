# pytelegrambotapi
# python-dotenv

from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import keyboards as kb
from googletrans import Translator, LANGCODES
import database as db



load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = TeleBot(token=TOKEN)
translator = Translator()


# команда - /

# @bot.message_handler(commands=['start', 'help'])
# def start(message: types.Message):
#     chat_id = message.chat.id
#     first_name = message.from_user.first_name
#     if message.text == '/help':
#         bot.send_message(chat_id, 'Помощь по боту')
#     else:
#         bot.send_message(chat_id, f'Привет, {first_name}')
#
#
# @bot.message_handler(content_types=['text'])
# def answer(message: types.Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, message.text)



@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    db.add_user(first_name, chat_id)
    bot.send_message(chat_id, 'Выберите действие снизу',
                     reply_markup=kb.start_kb())


@bot.message_handler(func=lambda msg: msg.text == 'Start')
def start_translation(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, с которого хотите сделать перевод',
                     reply_markup=kb.lang_menu())
    bot.register_next_step_handler(message, get_lang_from)


def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, на который хотите сделать перевод',
                     reply_markup=kb.lang_menu())
    bot.register_next_step_handler(message, get_lang_to, message.text)


def get_lang_to(message: types.Message, lang_from):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напишите слово или текст для перевода',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)


def translate(message: types.Message, lang_from, lang_to):
    chat_id = message.chat.id
    _from = LANGCODES[lang_from.lower()]
    _to = LANGCODES[lang_to.lower()]
    translated_text = translator.translate(message.text, dest=_to, src=_from).text
    db.add_translation(_from, _to, message.text, translated_text, chat_id)
    bot.send_message(chat_id, translated_text)

def send_history(message):
    user_id = message.from.user.id
    if user_id in user_translations:
        history = "\n".join([f."{original}:{translated}" for original, translated in user_translations[user_id].items()])
        bot.reply_to(message, f"История переводов:\n{history}")
    else:
        bot.reply_to(message, f"История переводов пусто.")



bot.polling(none_stop=True)
