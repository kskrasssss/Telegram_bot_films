import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher, types 
# Створення бота, керування подіями(приймає апдейти і обробляє їх)
from aiogram.types import Message, CallbackQuery 
# для повідомлень і запитів з тг
from aiogram.fsm.storage.memory import MemoryStorage
# Збереження станів FSM(state1 --> wait for answer --> state2 --> ...)
from aiogram.filters import CommandStart, Command
# фільтри для обробки команд
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# Імпортує класи та утиліти для створення клавіатур з кнопками
from aiogram.client.default import DefaultBotProperties
# для встановлення властивостей бота(форматування тексту за допомоги ParseMode)
from aiogram.enums import ParseMode
# Форматування повідомлень(html)

from aiogram import Router
# для маршрутизації повідомлень та команд

from commands import FILMS_COMMAND as films_command
from commands import START_COMMAND as start_command 
from commands import (
   FILMS_COMMAND,
   START_COMMAND,
   FILM_CREATE_COMMAND,
   BOT_COMMANDS,
   GENRE_BOT_COMMAND,
   MOOD_BOT_COMMAND,
)

from data import get_films
from keyboards import films_keyboard_markup, FilmCallback
# Обробка зворотніх викликів

from models import Film
# Описує об'єкт фільму
from aiogram.types import URLInputFile
# URL

from aiogram.fsm.context import FSMContext
# для представлення контексту поточного стану FSM(зберігає дані, оновлювати стани і змінювати їх для користувача)
from aiogram.fsm.state import State, StatesGroup
# для визначення та групування станів FSM

from data import get_films, add_film, get_unique_genres

from aiogram.types import ReplyKeyboardRemove
# дозволяє видаляти клавіатур, коли вона не потрібна

TOKEN = '7915854158:AAHiioHgdxpKyciXd1naKhbghkvwdJJK6-I'
logging.basicConfig(level = logging.INFO)

bot = Bot(token = TOKEN)
dp = Dispatcher(storage = MemoryStorage())

ADMINS = [1127328647]

async def on_startup(dp):
    logging.info('Bot is running')
# Запуск

@dp.message(Command(start_command))
async def start(message: Message):
    await message.answer(
        f'Привіт, {message.from_user.full_name}!\n'\
        'Обирай команду)'
    )
# Команда - вітання

router = Router()
# створює екземпляр для маршрутизації команд

class FilmForm(StatesGroup):
   name = State()
   description = State()
   rating = State()
   genre = State()
   mood = State()
   actors = State()
   poster = State()
# визначає послідовні стани для створення фільму.

@router.message(Command(films_command))
async def films_handler(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        text = f'Оберіть фільм.',
        reply_markup=markup
    )
# Обробник команди films, який отримує список фільмів та показує їх користувачу через клавіатуру.

dp.include_router(router)
# Додає router до Dispatcher(усі маршрути, що є в роутерія. передаються діспатчеру)

# Коли користувач надсилає повідомлення, воно потрапляє до диспетчера.
# Диспетчер перевіряє, в якому роутері є відповідний обробник, і запускає потрібну функцію.

@dp.callback_query(FilmCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    film_id = callback_data.id
    film_data = get_films(film_id=film_id)
    film = Film(**film_data)


    text = f"Фільм: {film.name}\n" \
           f"Опис: {film.description}\n" \
           f"Рейтинг: {film.rating}\n" \
           f"Жанр: {film.genre}\n" \
           f"Актори: {', '.join(film.actors)}\n"
   
    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            film.poster,
            filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
        )
    )
# Функція, що обробляє зворотний виклик при виборі фільму та показує деталі фільму користувачу.



@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext) -> None:
   await state.set_state(FilmForm.name)
   await message.answer(
       f"Введіть назву фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )
# Запуск процесу додавання фільму. Переносить дію до назви

@dp.message(FilmForm.name)
async def film_name(message: Message, state: FSMContext) -> None:
   await state.update_data(name=message.text)
   await state.set_state(FilmForm.description)
   await message.answer(
       f"Введіть опис фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )
# Обробляє введення назви користувачем, переходить до наступного стану

@dp.message(FilmForm.description)
async def film_description(message: Message, state: FSMContext) -> None:
   await state.update_data(description=message.text)
   await state.set_state(FilmForm.rating)
   await message.answer(
       f"Вкажіть рейтинг фільму від 0 до 10.",
       reply_markup=ReplyKeyboardRemove(),
   )
# Обробляє введення опису користувачем, переходить до наступного стану

@dp.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
   await state.update_data(rating=float(message.text))
   await state.set_state(FilmForm.genre)
   await message.answer(
       f"Введіть жанр фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )
# Обробляє введення рейтингу користувачем, переходить до наступного стану

@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
   await state.update_data(genre=message.text)
   await state.set_state(FilmForm.mood)
   await message.answer(
       text=f"Введіть настрій фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )
# Обробляє введення назви жанру користувачем, переходить до наступного стану

@dp.message(FilmForm.mood)
async def film_name(message: Message, state: FSMContext) -> None:
   await state.update_data(mood=message.text)
   await state.set_state(FilmForm.actors)
   await message.answer(
       f"Введіть акторів фільму через роздільник ', '\n"
       + "<b>Обов'язкова кома та відступ після неї.</b>",
       reply_markup=ReplyKeyboardRemove(),
   )
# Обробляє введення настрою фільму, переходить до наступного стану

@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
   await state.update_data(actors=[x for x in message.text.split(", ")])
   await state.set_state(FilmForm.poster)
   await message.answer(
       f"Введіть посилання на постер фільму.",
       reply_markup=ReplyKeyboardRemove(),
   )
# Обробляє введення списку акторів користувачем, переходить до наступного стану

@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
   data = await state.update_data(poster=message.text)
   film = Film(**data)
   add_film(film.model_dump())
   await state.clear()
   await message.answer(
       f"Фільм {film.name} успішно додано!",
       reply_markup=ReplyKeyboardRemove(),
   )
# Обробляє введення силки на постер користувачем


def get_unique_genres():
    films = get_films()
    return list({film['genre'] for film in films})
# Повертає унікальний список кнопок - жанрів

@dp.message(GENRE_BOT_COMMAND)
async def genre_handler(message: Message):
    genres = get_unique_genres()
    builder = InlineKeyboardBuilder()
    for genre in genres:
        builder.button(text=genre, callback_data=f"genre_{genre}")
    builder.adjust(1, repeat=True)  # Розміщуємо кнопки в стовпчик по одному
    await message.answer("Оберіть жанр:", reply_markup=builder.as_markup())
# Обробник команди genre, яка показує усі жанри для вибору

@dp.callback_query(lambda call: call.data.startswith("genre_"))
async def show_films_by_genre(callback: CallbackQuery):
    genre = callback.data.split("genre_")[1]
    films = get_films()
    filtered_films = [film for film in films if film["genre"] == genre]

    if filtered_films:
        builder = InlineKeyboardBuilder()
        for film in filtered_films:
            builder.button(text=film["name"], callback_data=f"film_{film['name']}")
        builder.adjust(1)

        await callback.message.answer(
            f"Оберіть фільм у жанрі '{genre}':", 
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.answer("Немає фільмів у цьому жанрі.")
# Обробник для вибору фільму після вибору жанру


@dp.callback_query(lambda call: call.data.startswith("film_"))
async def callb_film(callback: CallbackQuery):
    film_name = callback.data.split("film_")[1]
    films = get_films()
    film_data = next((film for film in films if film["name"] == film_name), None)
    
    if film_data:
        film = Film(**film_data)
        text = (
            f"Фільм: {film.name}\n"
            f"Опис: {film.description}\n"
            f"Рейтинг: {film.rating}\n"
            f"Жанр: {film.genre}\n"
            f"Актори: {', '.join(film.actors)}\n"
        )
       
        await callback.message.answer_photo(
            caption=text,
            photo=URLInputFile(
                film.poster,
                filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
            )
        )
    else:
        await callback.message.answer("Фільм не знайдено.")
# Обробник для відображення інформації про фільм за жанром


@dp.message(Command("mood"))
async def mood_handler(message: Message):
    moods = [
        ("Веселий", "happy"),
        ("Саркастичний", "sarcastic"),
        ("Усе надоїло (хочеться гострих відчуттів)", "adventure"),
        ("Сумний (хочеться плакати)", "sad"),
        ("Романтичний (хочеться любові)", "romantic"),
        ("Злий (хоче помсти)", "angry")
    ]

    builder = InlineKeyboardBuilder()
    for mood_text, mood_value in moods:
        builder.button(text=mood_text, callback_data=f"mood_{mood_value}")
    builder.adjust(1)

    await message.answer("Який у Вас настрій?", reply_markup=builder.as_markup())
# Обробник для визначення настрою користувача, через кнопки

@dp.callback_query(lambda call: call.data.startswith("mood_"))
async def show_films_by_mood(callback: CallbackQuery):
    mood = callback.data.split("mood_")[1]
    films = get_films()
    # Фільтруємо фільми відповідно до настрою
    filtered_films = [film for film in films if film["mood"] == mood]

    if filtered_films:
        builder = InlineKeyboardBuilder()
        for film in filtered_films:
            builder.button(text=film["name"], callback_data=f"film_{film['name']}")
        builder.adjust(1)

        await callback.message.answer(
            f"Оберіть фільм для настрою '{mood}':", 
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.answer("Немає фільмів для цього настрою.")
# Обробник для вибору фільму після вибору настрою

@dp.callback_query(lambda call: call.data.startswith("film_mood_"))
async def show_film_info_by_mood(callback: CallbackQuery):
    film_name = callback.data.split("film_mood_")[1]
    films = get_films()
    film_data = next((film for film in films if film["name"] == film_name), None)
    
    if film_data:
        film = Film(**film_data)
        text = (
            f"Фільм: {film.name}\n"
            f"Опис: {film.description}\n"
            f"Рейтинг: {film.rating}\n"
            f"Жанр: {film.genre}\n"
            f"Актори: {', '.join(film.actors)}\n"
        )
       
        await callback.message.answer_photo(
            caption=text,
            photo=URLInputFile(
                film.poster,
                filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
            )
        )
    else:
        await callback.message.answer("Фільм не знайдено.")
# Обробник для відображення інформації про фільм за настроєм


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot)
# Основна функція для запуску бота 


if __name__ == '__main__':
    asyncio.run(main())