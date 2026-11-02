import sqlite3


# Создание базы данных
conn = sqlite3.connect('DB.db')
cursor = conn.cursor()

cursor.execute('''
    DROP TABLE IF EXISTS film''')
cursor.execute('''
    DROP TABLE IF EXISTS hall''')
cursor.execute('''
    DROP TABLE IF EXISTS session''')
cursor.execute('''
    DROP TABLE IF EXISTS user''')
cursor.execute('''
    DROP TABLE IF EXISTS ticket''')

cursor.execute("PRAGMA foreign_keys = ON")

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS Film (
    film_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    duration INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Hall (
    hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR,
    rows_count INTEGER,
    seats_per_row INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER,
    hall_id INTEGER,
    start_time DATETIME,
    price DECIMAL,
    FOREIGN KEY (film_id) REFERENCES Film (film_id),
    FOREIGN KEY (hall_id) REFERENCES Hall (hall_id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR,
    password VARCHAR,
    email VARCHAR
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ticket (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_id INTEGER,
    row_number INTEGER,
    seat_number INTEGER,
    FOREIGN KEY (user_id) REFERENCES User (user_id),
    FOREIGN KEY (session_id) REFERENCES Session (session_id)
)
''')

    



# Добавление записи
cursor.execute("INSERT INTO Film (title,duration) VALUES ('Cheburashka_2',92)")
cursor.execute("INSERT INTO Film (title,duration) VALUES ('Spider-Man:_Brand_New_Day',145)")

cursor.execute("INSERT INTO Hall (name,rows_count,seats_per_row) VALUES ('Hall_1',15,10)")

cursor.execute("INSERT INTO User (username,password,email) VALUES ('admin', 'admin123', 'admin@cinema.ru')")
cursor.execute("INSERT INTO User (username,password,email) VALUES ('Elena','fgdfgdf','lena@email.com')")
cursor.execute("INSERT INTO User (username,password,email) VALUES ('Alexey','sjsjser','alex@email.com')")
cursor.execute("INSERT INTO User (username,password,email) VALUES ('Nikolay','wedfghnj','kolyan@gmail.com')")

cursor.execute("INSERT INTO Session (film_id,hall_id,start_time,price) VALUES (1,1,'2022-12-31 22:10',99999.99)")
cursor.execute("INSERT INTO Session (film_id,hall_id,start_time,price) VALUES (2,1,'2023-01-05 20:30',1000)")

cursor.execute("INSERT INTO Ticket (user_id,session_id,row_number,seat_number) VALUES (1,1,2,4)")
cursor.execute("INSERT INTO Ticket (user_id,session_id,row_number,seat_number) VALUES (1,2,1,5)")
cursor.execute("INSERT INTO Ticket (user_id,session_id,row_number,seat_number) VALUES (2,2,15,3)")
cursor.execute("INSERT INTO Ticket (user_id,session_id,row_number,seat_number) VALUES (3,2,15,5)")


# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()