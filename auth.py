from models import get_user_by_username
from getpass import getpass

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if not user:
        print("Ошибка: пользователь не найден.")
        return False
    
    if user['password'] == password:  
        return True
    else:
        print("Ошибка: неверный пароль.")
        return False

def login():
    username = input("Введите имя пользователя: ")
    password = getpass("Введите пароль: ")  
    if authenticate_user(username, password):
        print("Успешный вход")
        return username
    else:
        print("Ошибка входа")
        return None
