from repositories import hall_repository

def add_hall(name: str, rows_count: int, seats_per_row: int):
    if not name or rows_count <= 0 or seats_per_row <= 0:
        raise ValueError("Название зала и количество мест должны быть положительными")
    hall_repository.create(name, rows_count, seats_per_row)
    return hall_repository.get_all()[-1]

def get_all_halls():
    return hall_repository.get_all()

def get_hall(hall_id: int):
    hall = hall_repository.get_by_id(hall_id)
    if not hall:
        raise ValueError("Зал не найден")
    return hall

def update_hall(hall_id: int, name: str, rows_count: int, seats_per_row: int):
    if not hall_repository.get_by_id(hall_id):
        raise ValueError("Зал не найден")
    hall_repository.update(hall_id, name, rows_count, seats_per_row)

def delete_hall(hall_id: int):
    if not hall_repository.get_by_id(hall_id):
        raise ValueError("Зал не найден")
    hall_repository.delete(hall_id)