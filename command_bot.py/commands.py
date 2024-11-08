from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = 'start'
FILMS_COMMAND = 'films'

# Об'єкти команд
FILMS_BOT_COMMAND = BotCommand(command='films', description="Перегляд списку фільмів")
START_BOT_COMMAND = BotCommand(command='start', description="Почати розмову")
FILM_CREATE_COMMAND = Command("create_film")
GENRE_BOT_COMMAND = Command("genre")
MOOD_BOT_COMMAND = Command('mood')

# Список команд, який показуємо користувачам і оголушуєм в боті
BOT_COMMANDS = [
   BotCommand(command="films", description="Перегляд списку фільмів"),
   BotCommand(command="start", description="Почати розмову"),
   BotCommand(command="create_film", description="Додати новий фільм"),
   BotCommand(command="genre", description="Переглянути список фільмів за жанром"),
   BotCommand(command="mood", description="Переглянути фільми за настроєм")
]
