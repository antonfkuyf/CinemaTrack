from ui import console
from services import auth_service, film_service, ticket_service, hall_service, session_service
from repositories import session_repository, hall_repository, ticket_repository, user_repository

current_user = None
running = True

def start():
    global current_user, running
    while running:
        if not current_user:
            show_auth_menu()
        elif current_user.username == 'admin':
            show_admin_menu()
        else:
            show_main_menu()

def show_auth_menu():
    global current_user, running
    console.print_menu(["Авторизация", "Регистрация"])
    choice = console.get_choice(2)

    match choice:
        case 1:
            authenticate()
        case 2:
            register()
        case 0:
            running = False

def authenticate():
    global current_user
    username = input("Логин: ")
    password = input("Пароль: ")

    user = auth_service.authenticate(username, password)
    if user:
        current_user = user
        print(f"Добро пожаловать, {user.username}!")
    else:
        console.show_error("Неверный логин или пароль")

def register():
    username = input("Логин: ")
    password = input("Пароль: ")
    email = input("Email: ")

    try:
        user = auth_service.register(username, password, email)
        print("Регистрация успешна!")
    except Exception as e:
        console.show_error(str(e))

def show_main_menu():
    global current_user
    console.print_menu([
        "Просмотр афиши",
        "Покупка билета",
        "Мои билеты",
    ])
    choice = console.get_choice(3)

    if choice == 1:
        view_poster()
    elif choice == 2:
        purchase_ticket()
    elif choice == 3:
        view_my_tickets()
    elif choice == 0:
        current_user = None

def view_poster():
    films = film_service.get_all_films()
    rows = [(f.film_id, f.title, f.duration) for f in films]
    console.show_table(["Номер", "Название", "Длительность (мин)"], rows)
    return len(rows)

def view_sessions_by_film(film_id):
    sessions = session_repository.get_by_film(film_id)
    rows = [(s.session_id, s.film_id, s.hall_id, s.start_time, s.price) for s in sessions]
    console.show_table(["Номер", "Номер фильма", "Номер зала", "Время начала", "Цена"], rows)
    return [s[0] for s in rows]

def purchase_ticket():
    global current_user

    try:
        choice_film = console.get_choice(view_poster())
        if not choice_film:
            return
        choice_session = console.get_choice_by_nums([0]+view_sessions_by_film(choice_film))
        if not choice_session:
            return

        console.show_seats(choice_session)

        row_number = int(input("Номер ряда: "))
        seat_number = int(input("Номер места: "))

        ticket = ticket_service.purchase_ticket(
            current_user.user_id, choice_session, row_number, seat_number
        )
        price = session_repository.get_by_id(choice_session).price
        print(
            f"Билет куплен! ID: {ticket.ticket_id}, "
            f"Ряд: {ticket.row_number}, Место: {ticket.seat_number}, "
            f"Цена: {price} руб."
        )
    except Exception as e:
        console.show_error(str(e))

def view_my_tickets():
    global current_user
    tickets = ticket_service.get_user_tickets(current_user.user_id)
    if not tickets:
        print("У вас нет билетов")
        return
    rows = [(t.ticket_id, t.session_id, t.row_number, t.seat_number) for t in tickets]
    console.show_table(["ID", "Сеанс", "Ряд", "Место"], rows)




# ==================== МЕНЮ АДМИНИСТРАТОРА ====================
def show_admin_menu():
    global current_user
    console.print_menu([
        "Управление фильмами",
        "Управление залами",
        "Управление сеансами",
        "Управление билетами",
        "Управление пользователями",
    ])
    choice = console.get_choice(5)

    match choice:
        case 1:
            show_films_menu()
        case 2:
            show_halls_menu()
        case 3:
            show_sessions_menu()
        case 4:
            show_tickets_menu()
        case 5:
            show_users_menu()
        case 0:
            current_user = None

def show_films_menu():
    global current_user
    console.print_menu([
        "Добавить фильм",
        "Список фильмов",
        "Изменить фильм",
        "Удалить фильм",
    ])
    choice = console.get_choice(4)

    match choice:
        case 1:
            add_film()
        case 2:
            view_poster()
        case 3:
            update_film()
        case 4:
            delete_film()
        case 0:
            current_user = None

def add_film():
    title = input("Название: ")
    duration = int(input("Длительность: "))
    try:
        film = film_service.add_film(title, duration)
    except Exception as e:
        console.show_error(str(e))

def update_film():
    film_id = int(input("ID фильма: "))
    title = input("Новое название: ")
    duration = int(input("Новая длительность (мин): "))
    try:
        film_service.update_film(film_id, title, duration)
    except Exception as e:
        console.show_error(str(e))

def delete_film():
    film_id = int(input("ID фильма: "))
    try:
        film_service.delete_film(film_id)
    except Exception as e:
        console.show_error(str(e))

def show_halls_menu():
    global current_user
    console.print_menu([
        "Добавить зал",
        "Список залов",
        "Изменить зал",
        "Удалить зал",
    ])
    choice = console.get_choice(4)

    match choice:
        case 1:
            add_hall()
        case 2:
            view_halls()
        case 3:
            update_hall()
        case 4:
            delete_hall()
        case 0:
            current_user = None

def add_hall():
    name = input("Название зала: ")
    rows_count = int(input("Количество рядов: "))
    seats_per_row = int(input("Мест в ряду: "))
    try:
        hall = hall_service.add_hall(name, rows_count, seats_per_row)
        print(f"Зал добавлен! ID: {hall.hall_id}")
    except Exception as e:
        console.show_error(str(e))

def view_halls():
    halls = hall_service.get_all_halls()
    rows = [(h.hall_id, h.name, h.rows_count, h.seats_per_row) for h in halls]
    console.show_table(["ID", "Название", "Рядов", "Мест в ряду"], rows)

def update_hall():
    hall_id = int(input("ID зала: "))
    name = input("Новое название: ")
    rows_count = int(input("Новое количество рядов: "))
    seats_per_row = int(input("Новое количество мест в ряду: "))
    
    try:
        hall_service.update_hall(hall_id, name, rows_count, seats_per_row)
    except Exception as e:
        console.show_error(str(e))

def delete_hall():
    hall_id = int(input("ID зала: "))
    
    try:
        hall_service.delete_hall(hall_id)
    except Exception as e:
        console.show_error(str(e))
def show_sessions_menu():
    global current_user
    console.print_menu([
        "Создать сеанс",
        "Сеансы",
        "Удалить сеанс",
    ])
    choice = console.get_choice(3)

    match choice:
        case 1:
            add_session()
        case 2:
            view_sessions()
        case 3:
            delete_session()
        case 0:
            current_user = None

def add_session():
    film_id = int(input("ID фильма: "))
    hall_id = int(input("ID зала: "))
    start_time = input("Дата и время: ")
    price = float(input("Цена билета: "))
    
    try:
        session = session_service.add_session(film_id, hall_id, start_time, price)
        print(f"Сеанс создан! ID: {session.session_id}")
    except Exception as e:
        console.show_error(str(e))

def view_sessions():
    sessions = session_service.get_all_sessions()
    rows = [(s.session_id, s.film_id, s.hall_id, s.start_time, s.price) for s in sessions]
    console.show_table(["ID", "Фильм ID", "Зал ID", "Время", "Цена"], rows)
    choice = console.get_choice_by_nums([r[0] for r in rows])
    if not choice:
        return
    try:
        console.show_seats(choice)
    except Exception as e:
        console.show_error(str(e))

def delete_session():
    session_id = int(input("ID сеанса: "))
    
    try:
        session_service.delete_session(session_id)
    except Exception as e:
        console.show_error(str(e))

def show_tickets_menu():
    global current_user
    console.print_menu([
        "Добавить билет",
        "Список билетов",
        "Удалить билет",
    ])
    choice = console.get_choice(3)

    match choice:
        case 1:
            add_ticket()
        case 2:
            view_tickets()
        case 3:
            delete_ticket()
        case 0:
            current_user = None

def add_ticket():
    user_id = int(input("ID пользователя: "))
    session_id = int(input("ID сеанса: "))
    seat_number = int(input("Номер места: "))
    row_number = int(input("Номер ряда: "))
    
    try:
        ticket = ticket_service.purchase_ticket(user_id, session_id, seat_number, row_number)
        print(f"Билет добавлен. ID: {ticket.ticket_id}")
    except Exception as e:
        console.show_error(str(e))

def view_tickets():
    tickets = ticket_repository.get_all()
    rows = [(t.ticket_id, t.user_id, t.session_id, t.seat_number, t.row_number) for t in tickets]
    console.show_table(["ID", "ID пользователя", "ID сеанса", "Номер места", "Номер ряда"], rows)

def delete_ticket():
    ticket_id = int(input("ID билета: "))

    try:
        ticket_service.refund_ticket(ticket_id)
    except Exception as e:
        console.show_error(str(e))

def show_users_menu():
    global current_user
    console.print_menu([
        "Зарегистрировать пользователя",
        "Список пользователей",
        "Удалить пользователя",
    ])
    choice = console.get_choice(3)

    match choice:
        case 1:
            register_user()
        case 2:
            view_users()
        case 3:
            delete_user()
        case 0:
            current_user = None
def register_user():
    username = input("Логин: ")
    password = input("Пароль: ")
    email = input("Email: ")
    
    try:
        user = auth_service.register(username, password, email)
        print(f"Пользователь зарегистрирован! ID: {user.user_id}")
    except Exception as e:
        console.show_error(str(e))
def view_users():
    users = user_repository.get_all()
    rows = [(u.user_id, u.username, u.email) for u in users]
    console.show_table(["ID", "Логин", "Email"], rows)
def delete_user():
    user_id = int(input("ID пользователя: "))
    
    try:
        user_repository.delete(user_id)
    except Exception as e:
        console.show_error(str(e))