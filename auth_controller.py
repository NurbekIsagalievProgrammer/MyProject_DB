import json
from urllib.parse import parse_qs
from db_config import check_user  
from register import register_user
from main import generate_main_menu, generate_registration_page, generate_login_page

class AuthController:
    def __init__(self):
        pass

    def show_registration_page(self):
        return generate_registration_page()

    def show_login_page(self):
        return generate_login_page()

    def handle_login(self, post_data):
        data = parse_qs(post_data)  

        username = data.get('username', [None])[0]  
        password = data.get('password', [None])[0]  

        if check_user(username, password):
            return (200, generate_main_menu())
        else:
            return (401, json.dumps({"error": "Неверное имя пользователя или пароль"}))

    def handle_register(self, user_data):
        username = user_data.get('username')  
        password = user_data.get('password')  
        email = user_data.get('email')       

        activation_link = register_user(username, password, email)

        if activation_link:  
            return (201, generate_main_menu())  
        else:
            return (400, json.dumps({"error": "Ошибка регистрации"}))
        
    def handle_logout(self):
    
        self.send_response(302)  
        self.send_header('Location', '/registration') 
        self.end_headers()
