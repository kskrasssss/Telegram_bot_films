import logging  # для створення логів, відстеження та запису подій
import asyncio  # для роботи з асинхронними функціями та подіями
import sys  # для роботи з системними параметрами та функціями

from aiogram import Bot, Dispatcher, types  # Bot створює бота, Dispatcher керує подіями, приймає апдейти та обробляє їх
from aiogram.types import Message  # Тип для повідомлень Telegram
from aiogram.fsm.storage.memory import MemoryStorage  # Пам'ять для збереження станів користувачів (напр., FSM) у пам'яті
from aiogram.filters import CommandStart, Command  # Фільтри для обробки команд, наприклад, /start або кастомних команд
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton  # Клавіатура для інлайн-кнопок і їхніх властивостей
from aiogram.utils.keyboard import InlineKeyboardBuilder # допоміжний клас, який спрощує створення та налаштування клавіатур.
# InlineKeyboardButton(кнопка прив'язана до повідомлення, не там де клавіатура)


from aiogram.client.default import DefaultBotProperties  # Налаштування бота за замовчуванням
from aiogram.enums import ParseMode  # Форматування тексту, наприклад, Markdown або HTML

from aiogram import Router  # Маршрутизатор для організації обробки подій
from commands import FILMS_COMMAND as films_command  # Імпорт команди /films як змінної для використання в проєкті
from commands import START_COMMAND as start_command 
from commands import (
    FILMS_COMMAND,
    START_COMMAND,
    FILMS_BOT_COMMAND,
    START_BOT_COMMAND,
)


from data import get_films  # Функція для отримання списку фільмів
from keyboards import films_keyboard_markup  # Функція для створення клавіатури з кнопками фільмів

TOKEN = '7915854158:AAHiioHgdxpKyciXd1naKhbghkvwdJJK6-I'
logging.basicConfig(level = logging.INFO) # записує дані про події ІНФО і ВИЩЕ(ерор)

bot = Bot(token = TOKEN)
dp = Dispatcher(storage = MemoryStorage()) # ініціалізація диспатчера

ADMINS = [1127328647] # адміни


async def on_startup(dp):
    logging.info('Bot is running') # виведення логу про запуск бота

@dp.message(Command(start_command))
async def start(message: Message): # '/start'
    await message.answer(
        f'Привіт, {message.from_user.full_name}!\n'\
        'Обирай команду)'
    )

router = Router()

@router.message(Command(films_command))  # Створюємо фільтр безпосередньо в обробнику
async def films_handler(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        text = f'         Оберіть фільм.',
        reply_markup=markup
    )

dp.include_router(router)

async def main():
    await dp.start_polling(bot) # головна функція 

if __name__ == '__main__':
    asyncio.run(main()) # перевірка точки входу