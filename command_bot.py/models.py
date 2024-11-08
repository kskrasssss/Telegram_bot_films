from pydantic import BaseModel
# Pydantic дозволяє зручно визначати структури даних у Python 
# і автоматично перевіряти, що дані відповідають заданому формату

class Film(BaseModel):
    name: str
    description: str
    rating: float
    genre: str
    mood: str
    actors: list[str]
    poster: str
