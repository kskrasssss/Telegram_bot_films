import json

def get_films(file_path: str = "data.json", film_id: int | None = None) -> list[dict] | dict:
    with open(file_path, 'r') as fp:
        data = json.load(fp) # завантажує дані з json
        films = data.get("films", [])  # Отримуємо список фільмів з ключа "films"
        if film_id is not None and film_id < len(films):
            return films[film_id]
        return films

def add_film(
    film: dict,
    file_path: str = "data.json",
):
    # Завантажуємо весь JSON, щоб зберегти структуру файлу
    with open(file_path, 'r') as fp:
        data = json.load(fp)
        
    # Додаємо новий фільм до списку під ключем "films"
    data.setdefault("films", []).append(film)

    
    # Записуємо оновлений словник назад у файл
    with open(file_path, "w") as fp:
        json.dump(
            data,
            fp,
            indent=4, # відступи
            ensure_ascii=False, # підтримка неанглійських символів
        )

def get_unique_genres(file_path: str = "data.json") -> list[str]:
    with open(file_path, 'r') as fp:
        data = json.load(fp)
        films = data.get("films", []) # Отримуємо список фільмів з ключа "films"
        genres = {film["genre"] for film in films} # Отримуємо унікальні жанри з кожного фільму
        return list(genres)
