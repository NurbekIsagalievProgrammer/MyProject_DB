def generate_main_menu():
    activation_message = "<p>Ссылка для активации отправлена на ваш электронный адрес. Пожалуйста, перейдите по ней, чтобы активировать ваш аккаунт.</p>"
    return f"""
    <html>
        <head>
            <meta charset="UTF-8"> 
            <title>Главное меню</title>
            <script>
                function goToTable() {{
                    var table = document.getElementById("tableSelect").value;
                    if (table) {{
                        window.location.href = "/" + table;
                    }}
                }}
            </script>
        </head>
        <body>
            <h1>Главное меню</h1>
            {activation_message}  

            <!-- Выпадающий список для выбора таблиц -->
            <label for="tableSelect">Выберите таблицу для отображения:</label>
            <select id="tableSelect" onchange="goToTable()">
                <option value="">--Выберите таблицу--</option>
                <option value="animals">Животные</option>
                <option value="breeds">Породы</option>
                <option value="animaltypes">Типы животных</option>
                <option value="weightings">Взвешивания</option>
                <option value="users">Пользователи</option>
            </select>

            <form method="POST" action="/logout">
                <button type="submit">Выйти</button>
            </form>
        </body>
    </html>
    """




def generate_registration_page():
    return '''
        <html>
        <head><title>Регистрация</title></head>
        <body>
            <h1>Регистрация</h1>
            <form action="/register" method="post">
                <label for="username">Имя пользователя:</label><br>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Пароль:</label><br>
                <input type="password" id="password" name="password" required><br>
                <label for="email">Email:</label><br>
                <input type="email" id="email" name="email" required><br><br>
                <input type="submit" value="Зарегистрироваться">
            </form>
            <br>
            <a href="/login">Войти</a>
        </body>
        </html>
    '''

def generate_login_page():
    return '''
        <html>
        <head><title>Авторизация</title></head>
        <body>
            <h1>Авторизация</h1>
            <form action="/login" method="post">
                <label for="username">Имя пользователя:</label><br>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Пароль:</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Войти">
            </form>
            <br>
            <a href="/">Регистрация</a>
        </body>
        </html>
    '''
