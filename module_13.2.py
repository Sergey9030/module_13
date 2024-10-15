from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


api = "7894373187:AAG6EizTKiQDfLof5qLUszC9oeTyDhckb6k"
bot = Bot(token=api) # Бот
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер

@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_messsage(message):
    print('ведите команду /start, чтобы начать общение.')

# Дальше ничего выполняться не будет

@dp.message_handler(text=['Привет', 'hl'])
async def hello_message(message):
    print('Привет message')

@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Start message')

@dp.message_handler()
async def all_message(message):
    print('Пришло сообщение')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
