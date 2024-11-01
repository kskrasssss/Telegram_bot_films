# Модуль в якому оголошені всі необхідні команди(та їх фільтри)
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = 'start'
FILMS_COMMAND = 'films'

FILMS_BOT_COMMAND = BotCommand(command='films', description="Перегляд списку фільмів")
START_BOT_COMMAND = BotCommand(command='start', description="Почати розмову")