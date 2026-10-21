import sqlite3

# Создание базы данных (файл)
conn = sqlite3.connect('DB.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS Film (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    duration INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Hall (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR,
    rows_count INTEGER,
    seats_per_row INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER,
    hall_id INTEGER,
    start_time DATETIME,
    price DECIMAL,
    FOREIGN KEY (film_id) REFERENCES Film (id),
    FOREIGN KEY (hall_id) REFERENCES Hall (id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Seat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hall_id INTEGER NOT NULL,
    row_number INTEGER,
    seat_number INTEGER,
    FOREIGN KEY (hall_id) REFERENCES Hall (id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR,
    password VARCHAR,
    email VARCHAR
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_id INTEGER,
    seat_id INTEGER,
    price DECIMAL,
    FOREIGN KEY (user_id) REFERENCES User (id),
    FOREIGN KEY (session_id) REFERENCES Session (id),
    FOREIGN KEY (seat_id) REFERENCES Seat (id)
)
''')





# Добавление записи
cursor.execute("INSERT INTO Film (title,duration) VALUES ('HUY',6)")
cursor.execute("INSERT INTO Hall (name,rows_count,seats_per_row) VALUES ('hz',15,10)")
cursor.execute("INSERT INTO Seat (hall_id,row_number,seat_number) VALUES (1,3,6)")
cursor.execute("INSERT INTO User (username,password,email) VALUES ('Pizda','fgdfgdf','pizda@email.com')")
cursor.execute("INSERT INTO Session (film_id,hall_id,start_time,price) VALUES (1,1,'4434-12-31',6)")
cursor.execute("INSERT INTO Ticket (user_id,session_id,seat_id,price) VALUES (1,1,1,6)")


# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()