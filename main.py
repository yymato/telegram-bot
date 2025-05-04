# Импортируем необходимые классы.
import logging

import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def translate_word(word, source_lang='ru', target_lang='en'):
    url = f"https://api.mymemory.translated.net/get?q={word}&langpair={source_lang}|{target_lang}"
    response = requests.get(url)
    if response:
        data = response.json()
        if data.get('responseData'):
            return data['responseData']['translatedText'].lower()
    return None


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token('8014154157:AAEYnWKWkRvGVL_rqlbs6SRKew20u9g2d1I').build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    # Регистрируем обработчик в приложении.
    application.add_handler(MessageHandler(filters.TEXT, echo))

    # Запускаем приложение.
    application.run_polling()


async def echo(update, context):
    reply_keyboard = [['сменить направление перевода']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    if 'direction' not in context.user_data:
        context.user_data['direction'] = 'ru-en'
    text = update.message.text.lower()
    print(text)
    if text == 'сменить направление перевода':
        context.user_data['direction'] = 'ru-en' if context.user_data['direction'] == 'en-ru' else 'en-ru'
        await update.message.reply_text(f'направление перевода {context.user_data['direction']}', reply_markup=markup)
    else:
        await update.message.reply_text(translate_word(text, context.user_data['direction'].split('-')[0],
                                                       context.user_data['direction'].split('-')[1]),
                                        reply_markup=markup)


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
