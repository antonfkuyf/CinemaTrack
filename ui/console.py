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