from repositories import ticket_repository, session_repository, hall_repository
from services import ticket_service
def print_menu(menu_items):
    print("\n=== Меню ===")
    for i, item in enumerate(menu_items, 1):
        print(f"{i}. {item}")
    print("0. Выход")

def get_choice(max_choice: int):
    while True:
        try:
            choice = int(input("Выбор: "))
            if 0 <= choice <= max_choice:
                return choice
            print(f"Введите число от 0 до {max_choice}")
        except ValueError:
            print("Неверный ввод")

def get_choice_by_nums(nums):
    while True:
        try:
            choice = int(input("Выбор: "))
            if choice in nums:
                return choice
            print(f"Введите число из списка: {nums}")
        except ValueError:
            print("Неверный ввод")

def show_error(error: str):
    print(f"\nОшибка: {error}")

def show_table(headers, rows):
    print("\n" + "-" * 60)
    print(" | ".join(str(h) for h in headers))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(cell) for cell in row))
    print("-" * 60)

def show_seats(session_id: int):
    rows = ticket_repository.get_seats_by_session(session_id)
    hall_id = session_repository.get_by_id(session_id).hall_id
    rows_count = hall_repository.get_by_id(hall_id).rows_count
    seats_per_row = hall_repository.get_by_id(hall_id).seats_per_row

    seats = []
    count_seats = ticket_service.count_seats(session_id)
    if not count_seats:
        raise ValueError("Мест больше нет(")
    if True:
        for i in range(1, rows_count+1):
            row = list(' '*seats_per_row)
            num = 0
            for j in rows:
                if j[1] == i:
                    row[j[0]-1] = '.'
                    num+=1
            seats+=row
            print('|' + "|".join(row) + '|')