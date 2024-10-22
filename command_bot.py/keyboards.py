from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    name: str

def films_keyboard_markup(films_list:list[dict], offset:int|None = None, skip:int|None = None):
    pass
   
    # Створюємо та налаштовуємо клавіатуру
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)


    for index, film_data in enumerate(films_list):
        # Створюємо об'єкт CallbackData
        callback_data = FilmCallback(id=index, **film_data)
        # Додаємо кнопку до клавіатури
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )

    builder.adjust(1, repeat=True)
    return builder.as_markup()

