import asyncio
from threading import Thread
from flask import Flask
from models import BotLog, session
from bot import start_bot
from app import app as flask_app

def run_flask():
    flask_app.run(host='localhost', port=5000)

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Запускаем бота
    asyncio.run(start_bot())
