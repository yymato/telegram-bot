# Импортируем необходимые классы.
import logging
import string

from telegram.ext import Application, MessageHandler, filters, CommandHandler

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
user_sess = {}
poem = '''— Скажи-ка, дядя, ведь не даром
Москва, спаленная пожаром,
Французу отдана?
Ведь были ж схватки боевые,
Да, говорят, еще какие!'''

poem_without_punc = poem.lower()
for i in string.punctuation:
    if i == '-':
        continue
    poem_without_punc = poem_without_punc.replace(i, '')

poem_without_punc = poem_without_punc.replace('—', '').split('\n')
poem = poem.split('\n')
print(poem)
print(poem_without_punc)


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
    application.add_handler(MessageHandler(filters.TEXT, echo))

    # Запускаем приложение.
    application.run_polling()


async def start(update, context):
    context.user_data['poem_index'] = 0
    await update.message.reply_text(
        poem[context.user_data['poem_index']])


async def echo(update, context):
    text = update.message.text.lower()
    for i in string.punctuation:
        if i == '-':
            continue
        text = text.replace(i, '')
    text = text.replace('—', '')

    print(context.user_data['poem_index'])
    if len(poem) <= context.user_data['poem_index']:
        await update.message.reply_text('ы справился, Повторим? /start')
        return

    if text == poem_without_punc[context.user_data['poem_index'] + 1]:
        context.user_data['poem_index'] += 2
        if len(poem) - 1 < context.user_data['poem_index']:
            await update.message.reply_text('Ты справился, Повторим? /start')
        else:
            if len(poem) - 1 <= context.user_data['poem_index']:
                await update.message.reply_text(f'{poem[context.user_data['poem_index']]} '
                                                f'Ты справился, Повторим? /start')
            else:
                await update.message.reply_text(f'{poem[context.user_data['poem_index']]} ')
    else:
        await update.message.reply_text('нет, не так. Подсказка /suphler')


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
