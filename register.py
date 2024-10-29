import smtplib
import os
from email.mime.text import MIMEText
from db_config import connect_db
from dotenv import load_dotenv

load_dotenv()

def register_user(username, password, email):
    db = connect_db()
    if db is None:
        return None  
    
    cursor = db.cursor()
    
    try:
        sql = "INSERT INTO users (username, password, email, is_active, user_type) VALUES (%s, %s, %s, %s, %s)"
        val = (username, password, email, 0, 'user')  
        cursor.execute(sql, val)
        db.commit()
        
        activation_link = f"http://localhost:8000/activate?email={email}"
    
        send_activation_email(email, activation_link)  
        
        return activation_link  
    
    except Exception as err:
        print(f"Error: {err}")
        return None  
    finally:
        cursor.close()
        db.close()

def send_activation_email(to_email, activation_link):
    from_email = os.getenv("EMAIL_SENDER")  
    password = os.getenv("EMAIL_PASSWORD")  
    
    subject = "Activate your account"
    message = f"Click the link to activate your account: {activation_link}"
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Activation email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")  
