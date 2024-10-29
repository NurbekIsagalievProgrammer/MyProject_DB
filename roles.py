from models import get_user_by_username,get_user_by_id


def check_role(username, role):
    user = get_user_by_username(username)
    if not user:
        print("Пользователь не найден")
        return False

    user_type = user['user_type']
    
    if user_type == role:
        return True
    else:
        print(f"Ошибка: у пользователя недостаточно прав. Требуется роль {role}, текущая роль: {user_type}")
        return False

def is_admin(username):
    return check_role(username, 'admin')

def is_user(username):
    return check_role(username, 'user')

def check_user_role(user_id):
    user = get_user_by_id(user_id)  
    if not user:
        print("Пользователь не найден")
        return None

    return user['user_type'] 
