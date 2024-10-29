import re


def validate_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(email_regex, email):
        return True
    else:
        print("Ошибка: некорректный email.")
        return False


def validate_password(password):
    if len(password) < 8:
        print("Ошибка: пароль должен содержать не менее 8 символов.")
        return False
    if not any(char.isdigit() for char in password):
        print("Ошибка: пароль должен содержать хотя бы одну цифру.")
        return False
    if not any(char.isalpha() for char in password):
        print("Ошибка: пароль должен содержать хотя бы одну букву.")
        return False
    return True


def validate_user_input(username, password, email):
    if not username or len(username) < 3:
        print("Ошибка: имя пользователя должно содержать не менее 3 символов.")
        return False
    if not validate_password(password):
        return False
    if not validate_email(email):
        return False
    return True


def validate_animal_data(inventory_number, gender, name, arrival_date, age_months, breed_id, parent_id):
    if not inventory_number.isdigit():
        print("Ошибка: инвентарный номер должен содержать только цифры.")
        return False
    if gender not in ['male', 'female']:
        print("Ошибка: пол животного должен быть 'male' или 'female'.")
        return False
    if not name:
        print("Ошибка: имя не может быть пустым.")
        return False
    if not isinstance(age_months, int) or age_months < 0:
        print("Ошибка: возраст должен быть положительным числом.")
        return False
    
    if breed_id and not isinstance(breed_id, int):
        print("Ошибка: идентификатор породы должен быть целым числом.")
        return False
    if parent_id and not isinstance(parent_id, int):
        print("Ошибка: идентификатор родителя должен быть целым числом.")
        return False
    return True


def validate_animal_type_data(name):
    if not name or len(name) < 3:
        print("Ошибка: название типа животного должно содержать не менее 3 символов.")
        return False
    return True


def validate_breed_data(name, animaltype_id):
    if not name or len(name) < 3:
        print("Ошибка: название породы должно содержать не менее 3 символов.")
        return False
    if animaltype_id and not isinstance(animaltype_id, int):
        print("Ошибка: идентификатор типа животного должен быть целым числом.")
        return False
    return True


def validate_weighting_data(animal_id, date, weight_kg):
    if not isinstance(animal_id, int) or animal_id <= 0:
        print("Ошибка: ID животного должен быть положительным числом.")
        return False
    if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
        print("Ошибка: вес должен быть положительным числом.")
        return False
    return True


def validate_user_data(username, email, is_active, user_type):
    if not username or len(username) < 3:
        print("Ошибка: имя пользователя должно содержать не менее 3 символов.")
        return False
    if not validate_email(email):
        return False
    if not isinstance(is_active, bool):
        print("Ошибка: статус активности должен быть булевым значением (True/False).")
        return False
    if user_type not in ['admin', 'user']:  
        print("Ошибка: тип пользователя должен быть 'admin' или 'user'.")
        return False
    return True
