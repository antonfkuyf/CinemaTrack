from repositories import ticket_repository, session_repository, hall_repository
from models.models import Ticket

def purchase_ticket(user_id: int, session_id: int, row_number: int, seat_number: int):
    session = session_repository.get_by_id(session_id)
    if not session:
        raise ValueError("Сеанс не найден")

    hall = hall_repository.get_by_id(session.hall_id)
    if not hall:
        raise ValueError("Зал не найден")

    if row_number < 1 or row_number > hall.rows_count:
        raise ValueError(f"Неверный номер ряда. Допустимо: 1-{hall.rows_count}")

    if seat_number < 1 or seat_number > hall.seats_per_row:
        raise ValueError(f"Неверный номер места. Допустимо: 1-{hall.seats_per_row}")

    existing = ticket_repository.get_by_session_and_seat(session_id, row_number, seat_number)
    if existing:
        raise ValueError(f"Место уже занято: ряд {row_number}, место {seat_number}")

    ticket_repository.create(user_id, session_id, seat_number, row_number)
    return ticket_repository.get_by_session_and_seat(session_id, row_number, seat_number)

def get_user_tickets(user_id: int):
    return ticket_repository.get_by_user(user_id)

def refund_ticket(ticket_id: int):
    ticket = ticket_repository.get_by_id(ticket_id)
    if not ticket:
        raise ValueError("Билет не найден")
    ticket_repository.delete(ticket_id)