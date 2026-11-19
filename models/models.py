from dataclasses import dataclass
from datetime import datetime

@dataclass
class Film:
    film_id: int
    title: str
    duration: int

@dataclass
class Hall:
    hall_id: int
    name: str
    rows_count: int
    seats_per_row: int

@dataclass
class Session:
    session_id: int
    film_id: int
    hall_id: int
    start_time: datetime
    price: float

@dataclass
class User:
    user_id: int
    username: str
    password: str
    email: str

@dataclass
class Ticket:
    ticket_id: int
    user_id: int
    session_id: int
    seat_number: int
    row_number: int