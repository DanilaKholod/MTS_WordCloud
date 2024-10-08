from telebot import TeleBot, types
from wordcloud import WordCloud
from io import BytesIO
import random
import matplotlib.pyplot as plt
import model
import numpy as np
from PIL import Image
import matplotlib

matplotlib.use('agg')

# Токен бота
TOKEN = '7698122571:AAHDn4aS3kKntp8uk-c9edvxIsRyQqclCVk'
bot = TeleBot(TOKEN)

funny_responses = [
    "Давай без разговорчиков...",
    "Без CSV файла не разговариваю с людьми",
    "Давай вернемся к CSV!",
    "Не отвлекай меня! Я ведь жду твой CSV файл.",
    "Отправь мне CSV файл!"
]

def main_menu(chat_id):
    bot.send_message(chat_id, "Добро пожаловать! Для получения облака слов из отзывов сотрудников отправьте мне CSV файл.")


@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.mime_type != 'text/csv':
        bot.reply_to(message, "Я не принимаю такой формат файла. Отправьте CSV.")
        return
    try:
        # Получаем файл
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path

        # Скачиваем файл
        downloaded_file = bot.download_file(file_path)
        file_buffer = BytesIO(downloaded_file)
        model_output = model.model(file_buffer)

        # Отправка картинки
        bot.send_photo(message.chat.id, buf_cloud(model_output))
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, random.choice(funny_responses))

def buf_cloud(model_output):
    text = ""
    mask = np.array(Image.open('cloud.png'))
    bad_words = []
    with open("bad_words.txt", "r", encoding="utf-8") as f:
        for line in f:
            bad_words.append(line.rstrip())
    stop_words = model.stop_words
    stop_words.extend(bad_words)
    for word in model_output:
        text += (word + "  ") * model_output[word]
    wordcloud = WordCloud(width = 5000,
                          height = 5000,
                          random_state=1,
                          background_color='white',
                          margin=20,
                          colormap='plasma',
                          collocations=False,
                          mask=mask,
                          stopwords=stop_words).generate(text)
    buf = BytesIO()
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

# Запуск бота
bot.polling(none_stop=True, interval=0)
