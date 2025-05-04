# Импортируем необходимые классы.
import logging

import requests
from telegram.ext import Application, MessageHandler, filters

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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


def get_coords_from_geocoder(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]

    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    self_point = f'{toponym_longitude},{toponym_lattitude}'
    return self_point, toponym['description']


async def echo(update, context):
    text = update.message.text.lower()
    coords = get_coords_from_geocoder(text)

    server = "http://static-maps.yandex.ru/v1?"

    param = {'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
             'll': coords[0],
             'z': 15}
    response = requests.get(server, params=param)

    if response.status_code == 200:
        await update.message.reply_photo(
            photo=response.content,
            caption=coords[1],
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text('Не удалось загрузить карту.')



# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
