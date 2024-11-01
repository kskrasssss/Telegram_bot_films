from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

# CallbackData в інлайні - 
class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    name: str

def films_keyboard_markup(films_list:list[dict], offset:int|None = None, skip:int|None = None):
    
   
    # Створюємо та налаштовуємо клавіатуру
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    for index, film in enumerate(films_list):
    # Отримуємо лише назву фільму
        callback_data = FilmCallback(id=index, name=film["name"])
        builder.button(
            text=f"{film['name']}",
            callback_data=callback_data.pack())


    builder.adjust(1, repeat=True)
    return builder.as_markup()


    builder.adjust(1, repeat=True)
    return builder.as_markup()

