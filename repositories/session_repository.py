import sqlite3
from models.models import Session

def _map(row) -> Session:
    return Session(*row)

def get_connection():
    conn = sqlite3.connect('DB.db')
    return conn

def create(film_id: int, hall_id: int, start_time: str, price: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Session(
            film_id,
            hall_id,
            start_time,
            price
        )
        VALUES (?, ?, ?, ?)
    """, (film_id, hall_id, start_time, price))
    conn.commit()
    conn.close()

def get_by_id(session_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT session_id,
               film_id,
               hall_id,
               start_time,
               price
        FROM Session
        WHERE session_id = ?
    """, (session_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_film(film_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT session_id,
               film_id,
               hall_id,
               start_time,
               price
        FROM Session
        WHERE film_id = ?
    """, (film_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT session_id,
               film_id,
               hall_id,
               start_time,
               price
        FROM Session
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(session_id: int, film_id: int, hall_id: int, start_time: str, price: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Session
        SET film_id = ?,
            hall_id = ?,
            start_time = ?,
            price = ?
        WHERE session_id = ?
    """, (film_id, hall_id, start_time, price, session_id))
    conn.commit()
    conn.close()

def delete(session_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Session
        WHERE session_id = ?
    """, (session_id,))
    conn.commit()
    conn.close()