from repositories import session_repository, film_repository, hall_repository

def add_session(film_id: int, hall_id: int, start_time: str, price: float):
    film = film_repository.get_by_id(film_id)
    if not film:
        raise ValueError("Фильм не найден")
    
    hall = hall_repository.get_by_id(hall_id)
    if not hall:
        raise ValueError("Зал не найден")
    
    if price <= 0:
        raise ValueError("Цена должна быть положительной")
    
    session_repository.create(film_id, hall_id, start_time, price)
    return session_repository.get_all()[-1]

def get_all_sessions():
    return session_repository.get_all()

def get_session(session_id: int):
    session = session_repository.get_by_id(session_id)
    if not session:
        raise ValueError("Сеанс не найден")
    return session

def update_session(session_id: int, film_id: int, hall_id: int, start_time: str, price: float):
    if not session_repository.get_by_id(session_id):
        raise ValueError("Сеанс не найден")
    session_repository.update(session_id, film_id, hall_id, start_time, price)

def delete_session(session_id: int):
    if not session_repository.get_by_id(session_id):
        raise ValueError("Сеанс не найден")
    session_repository.delete(session_id)