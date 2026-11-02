import sqlite3
from models.models import Ticket

def _map(row) -> Ticket:
    return Ticket(*row)

def get_connection():
    conn = sqlite3.connect('DB.db')
    return conn

def create(user_id: int, session_id: int, seat_number: int, row_number: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Ticket(
            user_id,
            session_id,
            seat_number,
            row_number
        )
        VALUES (?, ?, ?, ?)
    """, (user_id, session_id, seat_number, row_number))
    conn.commit()
    conn.close()

def get_by_id(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ticket_id,
               user_id,
               session_id,
               seat_number,
               row_number
        FROM Ticket
        WHERE ticket_id = ?
    """, (ticket_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_session_and_seat(session_id: int, row_number: int, seat_number: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ticket_id,
               user_id,
               session_id,
               seat_number,
               row_number
        FROM Ticket
        WHERE session_id = ? AND row_number = ? AND seat_number = ?
    """, (session_id, row_number, seat_number))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ticket_id,
               user_id,
               session_id,
               seat_number,
               row_number
        FROM Ticket
        WHERE user_id = ?
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ticket_id,
               user_id,
               session_id,
               seat_number,
               row_number
        FROM Ticket
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(ticket_id: int, user_id: int, session_id: int, seat_number: int, row_number: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Ticket
        SET user_id = ?,
            session_id = ?,
            seat_number = ?,
            row_number = ?
        WHERE ticket_id = ?
    """, (user_id, session_id, seat_number, row_number, ticket_id))
    conn.commit()
    conn.close()

def delete(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Ticket
        WHERE ticket_id = ?
    """, (ticket_id,))
    conn.commit()
    conn.close()