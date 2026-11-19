from repositories import user_repository
from models.models import User

def register(username: str, password: str, email: str):
    if not username or not password:
        raise ValueError("Логин и пароль обязательны")

    existing = user_repository.get_by_username(username)
    if existing:
        raise ValueError("Пользователь с таким логином уже существует")

    user_repository.create(username, password, email)
    created = user_repository.get_by_username(username)
    return created

def authenticate(username: str, password: str):
    user = user_repository.get_by_username(username)
    if not user:
        return None

    if user.password != password:
        return None

    return user