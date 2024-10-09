import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from models import BotLog, session


API_TOKEN = '7006803480:AAEqvL8PcdpzPW9pFFgcXzUEauZw0BSlMuw'
WEATHER_API_KEY = '09c4fe1542148093d8ad69b26f97dedc'


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Напишите ваш город: ?')

@dp.message_handler(lambda message: True)
async def text_message_handler(message: types.Message):
    user_id = message.chat.id
    command = message.text
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={command}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            await message.answer(f"Температура в {command}: {temperature}°C\nОписание: {description}")
            log_entry = BotLog(user_id=user_id, username=message.from_user.username, command=command, message=message.text,
                               response=f"Температура: {temperature}°C, Описание: {description}")
            session.add(log_entry)
            session.commit()
        else:
            await message.answer(f"Не найден город - {message.text}")
            log_entry = BotLog(user_id=user_id, username=message.from_user.username, command=command, message=message.text,
                               response="Ошибка: Не найден город")
            session.add(log_entry)
            session.commit()
    except Exception as error:
        await message.answer(str(error))
        log_entry = BotLog(user_id=user_id, username=message.from_user.username, command=command, message=message.text,
                           response=str(error))
        session.add(log_entry)
        session.commit()

async def start_bot():
    print("Бот запущен.")
    await dp.start_polling()
