# Импортируем необходимые классы.
import json
import logging
import random

from telegram.ext import Application, MessageHandler, filters, CommandHandler

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
with open('data.json', 'r', encoding='utf-8') as f:
    question = json.load(f)['test']


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

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(MessageHandler(filters.TEXT, echo))

    # Запускаем приложение.
    application.run_polling()


async def start(update, context):
    context.user_data['last_indexes'] = [random.randint(0, len(question) - 1)]
    context.user_data['right_response'] = 0
    quest = question[context.user_data['last_indexes'][0]]['question']
    await update.message.reply_text(f'Пройдите опрос. {quest}')


async def echo(update, context):
    try:
        text = update.message.text.lower()
        if text == question[context.user_data['last_indexes'][-1]]['response']:
            context.user_data['right_response'] += 1
            if len(context.user_data['last_indexes']) == 10:
                await update.message.reply_text(f'Конец. Количество правильных ответов '
                                                f'{context.user_data['right_response']}')
                return

        while True:
            index = random.randint(0, len(question) - 1)
            if index not in context.user_data['last_indexes']:
                break
        context.user_data['last_indexes'].append(index)
        quest = question[context.user_data['last_indexes'][-1]]['question']
        await update.message.reply_text(quest)
    except KeyError:
        await update.message.reply_text('Я не знаю, что делать')


async def stop(update, context):
    context.user_data.pop('last_indexes', None)
    context.user_data.pop('right_response', None)
    await update.message.reply_text('тест сброшен')


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
