import json
# from films import films

# Завантажує список фіьмів з файлу data.json, отримання даних про фільми
def get_films(file_path: str = "data.json", film_id: int | None = None) -> list[dict] | dict:
    with open(file_path, 'r') as fp:
        data = json.load(fp)
        films = data.get("films", [])  # Отримуємо список фільмів з ключа "films"
        if film_id is not None and film_id < len(films):
            return films[film_id]
        return films
