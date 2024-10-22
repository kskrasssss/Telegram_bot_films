import logging # для логів, відслідковування подій
import asyncio # для роботи з асихронними функціями/подіями
import sys

from aiogram import Bot, Dispatcher # діспатчер обробляє всі події і повідомлення
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# from films import films
from commands import FILMS_COMMAND

from data import get_films
from keyboards import films_keyboard_markup

TOKEN = '7915854158:AAHiioHgdxpKyciXd1naKhbghkvwdJJK6-I'
logging.basicConfig(level = logging.INFO) # записує дані про події ІНФО і ВИЩЕ(ерор)

bot = Bot(token = TOKEN)
dp = Dispatcher(storage = MemoryStorage()) # ініціалізація диспатчера

ADMINS = [1127328647] # адміни

async def on_startup(dp):
    logging.info('Bot is running') # виведення логу про запуск бота

@dp.message(Command('start'))
async def start(message: Message): # '/start'
    await message.answer(
        f'Hi, {message.from_user.full_name}!\n'\
        'Choose a command.'
    )
    
@dp.message(FILMS_COMMAND)
async def films(message: Message):
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        f"Перелік фільмів. Натисніть на назву фільму для отримання деталей.",
        reply_markup=markup
    )


async def main():
    await dp.start_polling(bot) # головна функція 

if __name__ == '__main__':
    asyncio.run(main()) # перевірка точки входу