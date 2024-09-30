from telebot import TeleBot, types
from wordcloud import WordCloud
import json
from io import BytesIO

import matplotlib.pyplot as plt

# Токен бота
TOKEN = '7698122571:AAHDn4aS3kKntp8uk-c9edvxIsRyQqclCVk'
bot = TeleBot(TOKEN)


def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(chat_id, "Добро пожаловать! Загрузите CSV файл с отзывами сотрудников.",
                     reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        # Получаем файл
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)


        # Здесь должна быть модель


        # Заглушка в виде словаря
        model_output = {
                        "Зарплата": 34,
                        "Опыт": 25,
                        "Удовольствие": 14,
                        "Общение": 21
                        }

        # Отправка картинки
        bot.send_photo(message.chat.id, buf_cloud(model_output))

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

def buf_cloud(model_output):
    text = ""
    for word in model_output:
        text += (word + "  ") * model_output[word]
    wordcloud = WordCloud(width = 2000,
                          height = 1500,
                          random_state=1,
                          background_color='black',
                          margin=20,
                          colormap='Pastel1',
                          collocations=False).generate(text)
    buf = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

# Запуск бота
bot.polling(none_stop=True, interval=0)
