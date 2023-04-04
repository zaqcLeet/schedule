import telegram
from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup

# Устанавливаем токен бота
TOKEN = '6153443552:AAGeiAKM7UfBhPJFc1Ot2c9goHUXdoWtDq0'

# Создаем объект бота
bot = telegram.Bot(token=TOKEN)

# Функция для обработки команды /ras
def replaces(update, context):
    # получаем страницу с сайта
    try:
    response = requests.get('https://medcollege21.med.cap.ru/student/teoreticheskoe-obuchenie/zamena-zanyatij', timeout=10)
except requests.exceptions.ConnectTimeout:
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Sorry, the request has timed out. Please try again later.")
    return
    soup = BeautifulSoup(response.text, 'html.parser')

    # ищем все теги div с классом "attachfile_item_info"
    attachfiles = soup.find_all('div', {'class': 'attachfile_item_info'})

    # получаем последний тег и ссылку на файл
    last_attachfile = attachfiles[-1]
    link = last_attachfile.find('a').get('href')

    # формируем конечную ссылку
    final_link = f'https://medcollege21.med.cap.ru{link}'

    # скачиваем файл по ссылке
    file = requests.get(final_link)

    # отправляем файл пользователю
    chat_id = update.message.chat_id
    bot.send_document(chat_id=chat_id, document=file.content, filename='Замена.docx')

def start(update, context):
    # отправляем приветственное сообщение пользователю
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Привет, чтобы посмотреть замены выбери в меню команду или напиши /replaces")

# Создаем объект Updater
updater = Updater(token=TOKEN, use_context=True)

# Получаем объект диспетчера
dispatcher = updater.dispatcher

# Регистрируем обработчик команды /ras
dispatcher.add_handler(CommandHandler('replaces', replaces))
dispatcher.add_handler(CommandHandler('start', start))

# Запускаем бота
updater.start_polling()
