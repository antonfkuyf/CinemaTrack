import sqlite3
from models.models import User

def _map(row) -> User:
    return User(*row)

def get_connection():
    conn = sqlite3.connect('DB.db')
    return conn

def create(username: str, password: str, email: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO User(
            username,
            password,
            email
        )
        VALUES (?, ?, ?)
    """, (username, password, email))

    conn.commit()
    conn.close()

def get_by_id(user_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id,
               username,
               password,
               email
        FROM user
        WHERE user_id = ?
    """, (user_id,))

    row = cur.fetchone()

    conn.close()

    return _map(row) if row else None

def get_by_username(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id,
               username,
               password,
               email
        FROM User
        WHERE username = ?
    """, (username,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id,
               username,
               password,
               email
        FROM user
    """)

    rows = cur.fetchall()

    conn.close()

    return [_map(r) for r in rows]

def update(user_id: int, username: str,password: str, email: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user
        SET username = ?,
            password = ?,
            email = ?
        WHERE user_id = ?
    """, (username, password, email, user_id))

    conn.commit()
    conn.close()

def delete(user_id: int):

    conn = get_connection()
    cur = conn.cursor()

    conn.execute("""
    DELETE FROM user
    WHERE user_id = ?""", (user_id,))

    conn.commit()
    conn.close()