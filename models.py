from db_config import connect_db
from datetime import date
import mysql.connector 

# animal
def add_animal(inventory_number, gender, name, arrival_date, age_months, breed_id, parent_id=None):
    db = connect_db()
    cursor = db.cursor()
    
    try:
        sql = """
            INSERT INTO animal (inventory_number, gender, name, arrival_date, age_months, breed_id, parent_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (inventory_number, gender, name, arrival_date, age_months, breed_id, parent_id)
        cursor.execute(sql, val)
        db.commit()
        print("Animal added successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def get_animals():
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM animal")
    result = cursor.fetchall()
    
    animals = []
    for row in result:
        animal = {
            'id': row[0],
            'inventory_number': row[1],
            'gender': row[2],
            'name': row[3],
            'arrival_date': row[4].isoformat() if isinstance(row[4], date) else row[4],
            'age_months': row[5],
            'breed_id': row[6],
            'parent_id': row[7],
        }
        animals.append(animal)
    
    cursor.close()
    db.close()
    return animals

def update_animal(animal_id, name=None, age_months=None):
    db = connect_db()
    cursor = db.cursor()

    updates = []
    values = []
    
    if name is not None:  # Проверяем на None, чтобы поддержать обновление имени на пустую строку
        updates.append("name = %s")
        values.append(name)
    if age_months is not None:  # То же самое для возраста
        updates.append("age_months = %s")
        values.append(age_months)
    
    if updates:
        sql = f"UPDATE animal SET {', '.join(updates)} WHERE id = %s"
        values.append(animal_id)
        
        try:
            cursor.execute(sql, values)
            db.commit()
            print("Animal updated successfully")
        except Exception as e:
            print(f"Error updating animal: {str(e)}")  # Логируем ошибку
            db.rollback()  # Откатываем транзакцию в случае ошибки
    else:
        print("No updates provided for animal.")

    cursor.close()
    db.close()

def delete_animal(animal_id):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM animal WHERE id = %s", (animal_id,))
    db.commit()
    print("Animal deleted successfully")
    
    cursor.close()
    db.close()

# animaltype
def add_animaltype(name):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO animaltype (name) VALUES (%s)", (name,))
        db.commit()
        print("Animal type added successfully")
    except Exception as e:
        print(f"Error during insertion: {e}")
    finally:
        cursor.close()
        db.close()

def get_animaltypes():
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM animaltype")
    result = cursor.fetchall()
    
    animaltypes = []
    for row in result:
        animaltype = {
            'id': row[0],
            'name': row[1],
        }
        animaltypes.append(animaltype)
    
    cursor.close()
    db.close()
    return animaltypes

def update_animaltype(animaltype_id, name):
    db = connect_db()
    cursor = db.cursor()

    try:
        sql = "UPDATE animaltype SET name = %s WHERE id = %s"
        cursor.execute(sql, (name, animaltype_id))
        db.commit()
        print("Animal type updated successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def delete_animaltype(animaltype_id):
    db = connect_db()
    cursor = db.cursor()

    try:
        # Печатаем отладочное сообщение перед выполнением запроса
        print(f"Attempting to delete animal type with ID: {animaltype_id}")
        
        # Выполняем SQL-запрос на удаление
        cursor.execute("DELETE FROM animaltype WHERE id = %s", (animaltype_id,))
        
        # Проверяем, был ли удалён хотя бы один ряд
        if cursor.rowcount > 0:
            db.commit()  # Фиксируем изменения в базе данных
            print("Animal type deleted successfully")
            return {'message': "Animal type deleted successfully", 'status': 200}
        else:
            print(f"No animal type found with ID: {animaltype_id}")
            return {'message': f"No animal type found with ID {animaltype_id}", 'status': 404}

    except mysql.connector.Error as e:
        # Обработка ошибок и вывод отладочного сообщения
        print(f"Error during deletion: {e}")
        return {'message': f"Error: {str(e)}", 'status': 500}

    finally:
        # Закрываем курсор и соединение
        cursor.close()
        db.close()

# breed
def add_breed(name, animaltype_id):
    db = connect_db()
    cursor = db.cursor()
    
    try:
        sql = "INSERT INTO breed (name, animaltype_id) VALUES (%s, %s)"
        cursor.execute(sql, (name, animaltype_id))
        db.commit()
        print("Breed added successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def get_breeds():
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM breed")
    result = cursor.fetchall()
    
    breeds = []
    for row in result:
        breed = {
            'id': row[0],
            'name': row[1],
            'animaltype_id': row[2],
        }
        breeds.append(breed)
    
    cursor.close()
    db.close()
    return breeds

def update_breed(breed_id, name, animaltype_id):
    db = connect_db()
    cursor = db.cursor()

    try:
        sql = "UPDATE breed SET name = %s, animaltype_id = %s WHERE id = %s"
        cursor.execute(sql, (name, animaltype_id, breed_id))
        db.commit()
        print("Breed updated successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def delete_breed(breed_id):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM breed WHERE id = %s", (breed_id,))
        db.commit()
        print("Breed deleted successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

# Метод для добавления весовых данных
def add_weighting(animal_id, date, weight_kg):
    db = connect_db()
    cursor = db.cursor()
    
    try:
        sql = """
            INSERT INTO weighting (animal_id, date, weight_kg)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (animal_id, date, weight_kg))
        db.commit()
        print("Weighting added successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

# Метод для получения всех весовых данных
def get_weightings():
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM weighting")
    result = cursor.fetchall()
    
    weightings = []
    for row in result:
        weighting = {
            'id': row[0],
            'animal_id': row[1],
            'date': row[2].isoformat() if isinstance(row[2], date) else row[2],
            'weight_kg': row[3],
        }
        weightings.append(weighting)
    
    cursor.close()
    db.close()
    return weightings

# Метод для обновления весовых данных
def update_weighting(weighting_id, weight_kg=None, date=None):
    db = connect_db()
    cursor = db.cursor()

    try:
        updates = []
        params = []
        
        if weight_kg is not None:
            updates.append("weight_kg = %s")
            params.append(weight_kg)
        
        if date is not None:
            updates.append("date = %s")
            params.append(date)
        
        if updates:
            sql = f"UPDATE weighting SET {', '.join(updates)} WHERE id = %s"
            params.append(weighting_id)
            cursor.execute(sql, tuple(params))
            db.commit()
            print("Weighting updated successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

# Метод для удаления весовых данных
def delete_weighting(weighting_id):
    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM weighting WHERE id = %s", (weighting_id,))
        db.commit()
        print("Weighting deleted successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


# users
def add_user(username, password, email, is_active, user_type):
    db = connect_db()
    cursor = db.cursor()
    
    try:
        sql = """
            INSERT INTO users (username, password, email, is_active, user_type)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (username, password, email, is_active, user_type))
        db.commit()
        print("User added successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def get_users():
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    
    users = []
    for row in result:
        user = {
            'id': row[0],
            'username': row[1],
            'email': row[3],
            'is_active': row[4],
            'user_type': row[5],
        }
        users.append(user)

    cursor.close()
    db.close()
    return users

def update_user(user_id, username=None, password=None, email=None, is_active=None, user_type=None):
    db = connect_db()
    cursor = db.cursor()

    updates = []
    values = []
    
    if username:
        updates.append("username = %s")
        values.append(username)
    if password:
        updates.append("password = %s")
        values.append(password)
    if email:
        updates.append("email = %s")
        values.append(email)
    if is_active is not None:
        updates.append("is_active = %s")
        values.append(is_active)
    if user_type:
        updates.append("user_type = %s")
        values.append(user_type)

    if updates:
        sql = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        values.append(user_id)
        cursor.execute(sql, values)
        db.commit()
        print("User updated successfully")

    cursor.close()
    db.close()

def delete_user(user_id):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    print("User deleted successfully")
    
    cursor.close()
    db.close()
