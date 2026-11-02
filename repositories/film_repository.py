import sqlite3
from models.models import Film

def _map(row) -> Film:
    return Film(*row)

def get_connection():
    conn = sqlite3.connect('DB.db')
    return conn

def create(title: str, duration: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Film(
            title,
            duration
        )
        VALUES (?, ?)
    """, (title, duration))

    conn.commit()
    conn.close()

def get_by_id(film_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT film_id,
               title,
               duration
        FROM film
        WHERE film_id = ?
    """, (film_id,))

    row = cur.fetchone()

    conn.close()

    return _map(row) if row else None

def get_all():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT film_id,
               title,
               duration
        FROM Film
    """)

    rows = cur.fetchall()

    conn.close()

    return [_map(r) for r in rows]

def update(film_id: int, title: str,duration: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE film
        SET title = ?,
            duration = ?
        WHERE film_id = ?
    """, (title, duration, film_id))

    conn.commit()
    conn.close()

def delete(film_id: int):

    conn = get_connection()
    cur = conn.cursor()

    conn.execute("""
    DELETE FROM film
    WHERE film_id = ?""", (film_id,))

    conn.commit()
    conn.close()