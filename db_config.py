import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",        
            user="root",    
            password="Nurbek@123!",
            database="myproject_db"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def check_user(username, password):
    conn = connect_db()
    if conn is None:
        return False  

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            return False  

        stored_password = result[0]
        return password == stored_password  

    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
