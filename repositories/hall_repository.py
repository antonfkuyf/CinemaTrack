import sqlite3
from models.models import Hall

def _map(row) -> Hall:
    return Hall(*row)

def get_connection():
    conn = sqlite3.connect('DB.db')
    return conn

def create(name: str, rows_count: int, seats_per_row: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Hall(
            name,
            rows_count,
            seats_per_row
        )
        VALUES (?, ?, ?)
    """, (name, rows_count, seats_per_row))
    conn.commit()
    conn.close()

def get_by_id(hall_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT hall_id,
               name,
               rows_count,
               seats_per_row
        FROM Hall
        WHERE hall_id = ?
    """, (hall_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT hall_id,
               name,
               rows_count,
               seats_per_row
        FROM Hall
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(hall_id: int, name: str, rows_count: int, seats_per_row: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Hall
        SET name = ?,
            rows_count = ?,
            seats_per_row = ?
        WHERE hall_id = ?
    """, (name, rows_count, seats_per_row, hall_id))
    conn.commit()
    conn.close()

def delete(hall_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Hall
        WHERE hall_id = ?
    """, (hall_id,))
    conn.commit()
    conn.close()