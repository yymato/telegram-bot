# Импортируем необходимые классы.
import datetime
import logging
import random

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
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

    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(MessageHandler(filters.TEXT & ~ filters.COMMAND, echo))

    # Запускаем приложение.
    application.run_polling()


async def echo(update, context):
    flg = False
    if update.message.text == 'вернуться назад':
        reply_keyboard = [['/dice', '/timer']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        await update.message.reply_text('Выбирайте', reply_markup=markup)

    elif update.message.text == 'кинуть один шестигранный кубик':
        await update.message.reply_text(str(random.randint(1, 6)))
    elif update.message.text == 'кинуть 2 шестигранных кубика одновременно':
        await update.message.reply_text(f'{str(random.randint(1, 6))} {str(random.randint(1, 6))}')
    elif update.message.text == 'кинуть 20-гранный кубик':
        await update.message.reply_text(str(random.randint(1, 20)))
    elif update.message.text == '30 секунд':
        timer_1 = 30
        flg = True
    elif update.message.text == '1 минута':
        timer_1 = 60
        flg = True
    elif update.message.text == '5 минут':
        timer_1 = 300
        flg = True
    else:
        await update.message.reply_text('Я не знаю, что делать')
    if flg:
        chat_id = update.effective_message.chat_id

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        timer_log[str(chat_id)] = timer_1
        context.job_queue.run_once(task, timer_1, chat_id=chat_id, name=str(chat_id), data=timer_1)

        text = f'Вернусь через {timer_1} с.!'
        if job_removed:
            text += 'Старый таймер остановлена.'
        reply_keyboard = [['/close']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        await update.message.reply_text(text + 'Остановить таймер', reply_markup=markup)


TIMER = 5  # таймер на 5 секунд


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True



async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'{timer_log[str(context.job.chat_id)]} Время вышло!')


async def close(update, context):
    chat_id = update.effective_message.chat_id
    if remove_job_if_exists(str(chat_id), context):
        reply_keyboard = [['30 секунд', '1 минута',
                           '5 минут', 'вернуться назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        await update.message.reply_text('Выбирайте', reply_markup=markup)
    else:
        await update.message.reply_text('Нет активных таймеров')


async def start(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_text('Выбирайте', reply_markup=markup)


async def dice(update, context):
    reply_keyboard = [['кинуть один шестигранный кубик', 'кинуть 2 шестигранных кубика одновременно',
                       'кинуть 20-гранный кубик', 'вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_text('Выбирайте', reply_markup=markup)


async def timer(update, context):
    reply_keyboard = [['30 секунд', '1 минута',
                       '5 минут', 'вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_text('Выбирайте', reply_markup=markup)





async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
