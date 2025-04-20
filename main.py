# Импортируем необходимые классы.
import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
timer_log = {}


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.


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

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_room)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_room)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_room)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_room)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, five)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


async def start(update, context):
    markup = ReplyKeyboardMarkup([['вход']], one_time_keyboard=True)
    await update.message.reply_text(
        'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб', reply_markup=markup)

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


async def first_room(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    text = update.message.text
    if text == 'вход' or text == 'перейти в зал 1':
        markup = ReplyKeyboardMarkup([['перейти в зал 2', 'выход']], one_time_keyboard=True)
        await update.message.reply_text(
            'Зал 1 В данном зале представлено...(Описание). Можно перейти в зал 2 (кр. описание)', reply_markup=markup)
        return 2


async def second_room(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    text = update.message.text
    if text == 'перейти в зал 2':
        markup = ReplyKeyboardMarkup([['перейти в зал 3']], one_time_keyboard=True)
        await update.message.reply_text(
            'Зал 2 В данном зале представлено...(Описание). Можно перейти в зал 3 (кр. описание)', reply_markup=markup)
        return 3
    elif text == 'выход':
        await update.message.reply_text('Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!')
        return ConversationHandler.END


async def third_room(update, context):
    text = update.message.text
    if text == 'перейти в зал 3':
        markup = ReplyKeyboardMarkup([['перейти в зал 4', 'перейти в зал 1']], one_time_keyboard=True)
        await update.message.reply_text(
            'Зал 3 В данном зале представлено...(Описание). Можно перейти в зал 4 (кр. описание) и зал 1 (кр. описание)',
            reply_markup=markup)
        return 5


async def fourth_room(update, context):
    text = update.message.text
    if text == 'перейти в зал 4':
        markup = ReplyKeyboardMarkup([['перейти в зал 1']], one_time_keyboard=True)
        await update.message.reply_text(
            'Зал 4 В данном зале представлено...(Описание). Можно перейти в зал 1 (кр. описание)', reply_markup=markup)
        return 1


async def five(update, context):
    text = update.message.text
    if text == 'перейти в зал 1':
        return await first_room(update, context)

    elif text == 'перейти в зал 4':
        return await fourth_room(update, context)

async def stop(update, context):
    await update.message.reply_text("Диалог завершен.")
    return ConversationHandler.END

# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
