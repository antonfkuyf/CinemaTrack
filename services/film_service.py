from repositories import film_repository

def add_film(title: str, duration: int):
    if not title or duration <= 0:
        raise ValueError("Название и длительность обязательны")
    film_repository.create(title, duration)
    return film_repository.get_all()[-1]

def get_all_films():
    return film_repository.get_all()

def get_film(film_id: int):
    film = film_repository.get_by_id(film_id)
    if not film:
        raise ValueError("Фильм не найден")
    return film

def update_film(film_id: int, title: str, duration: int):
    if not film_repository.get_by_id(film_id):
        raise ValueError("Фильм не найден")
    film_repository.update(film_id, title, duration)

def delete_film(film_id: int):
    if not film_repository.get_by_id(film_id):
        raise ValueError("Фильм не найден")
    film_repository.delete(film_id)