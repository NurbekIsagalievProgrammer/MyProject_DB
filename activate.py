import mysql.connector
from db_config import connect_db
import cgi
import cgitb

cgitb.enable()

def activate_user(cursor, email):
    try:
        cursor.execute("SELECT id, is_active, user_type FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is None:
            return 404, "No user found with that email."

        user_id, is_active, user_type = result
        
        if is_active:
            return 400, "User is already active."
        
        sql = "UPDATE users SET is_active = %s, user_type = %s WHERE email = %s"
        cursor.execute(sql, (1, 'admin', email))

        return 200, "User activated successfully."
        
    except mysql.connector.Error as err:
        return 500, f"Error: {err}"

print("Content-Type: text/html\n")  

db = connect_db()
if db is None:
    print("<h1>Failed to connect to the database.</h1>")
else:
    cursor = db.cursor()
    form = cgi.FieldStorage()
    email = form.getvalue("email")  

    if email:
        email = email.strip().lower()
        status_code, result_message = activate_user(cursor, email) 
        db.commit()
        
        print(f"<h1>Status Code: {status_code}</h1>")
        print(f"<p>{result_message}</p>")
    else:
        print("<h1>Email is required for activation.</h1>")
    
    cursor.close()  
    db.close()
