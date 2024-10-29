import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import models
from auth_controller import AuthController
from db_config import connect_db
from activate import activate_user


class MainController(BaseHTTPRequestHandler):

    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def handle_error(self, status_code, message):
        self.send_error(status_code, message)
        print(f"Error: {message}")

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path in ('/', '/login'):
            self._show_page(path)
            return

        if path in ['/api/users', '/api/animals', '/api/animaltypes', '/api/breeds', '/api/weightings']:
            self._handle_json_response(self.handle_get(path))
            return

        if path.startswith('/api/activate'):
            self.handle_activate_request(parsed_path)
            return

        self.handle_error(404, "Маршрут не найден")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path in ['/api/register', '/api/login']:
            self.handle_auth(path)
        elif path in ['/api/animals', '/api/breeds', '/api/animaltypes', '/api/weightings', '/api/users']:
            self._handle_create(path)
        else:
            self.handle_error(404, "Маршрут не найден")

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 3 and path_parts[0] == "api":
            resource = path_parts[1]
            resource_id = path_parts[2]

            handlers = {
                'animals': self.handle_update_animal,
                'breeds': self.handle_update_breed,
                'animaltypes': self.handle_update_animaltype,
                'weightings': self.handle_update_weighting,
                'users': self.handle_update_user,
            }

            if resource in handlers:
                handlers[resource](resource_id)
            else:
                self.handle_error(404, "Ресурс не найден")
        else:
            self.handle_error(404, "Маршрут не найден")

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 3 and path_parts[0] == "api":
            resource = path_parts[1]
            resource_id = path_parts[2]

            handlers = {
                'animals': models.delete_animal,
                'breeds': models.delete_breed,
                'animaltypes': models.delete_animaltype,
                'weightings': models.delete_weighting,
                'users': models.delete_user,
            }

            if resource in handlers:
                try:
                    handlers[resource](int(resource_id))
                    self._set_headers(200)
                    self.wfile.write(json.dumps(
                        {"message": f"{resource.capitalize()} удален успешно"}).encode('utf-8'))
                except Exception as e:
                    self.handle_error(500, f"Ошибка удаления: {str(e)}")
            else:
                self.handle_error(404, "Ресурс не найден")
        else:
            self.handle_error(404, "Маршрут не найден")

    def handle_get(self, path):
        handlers = {
            '/api/users': models.get_users,
            '/api/animals': models.get_animals,
            '/api/animaltypes': models.get_animaltypes,
            '/api/breeds': models.get_breeds,
            '/api/weightings': models.get_weightings,
        }
        return handlers[path]()

    def _handle_json_response(self, content):
        self._set_headers(200)
        self.wfile.write(json.dumps(content).encode('utf-8'))

    def _handle_create(self, path):
        handlers = {
            '/api/animals': models.add_animal,
            '/api/breeds': models.add_breed,
            '/api/animaltypes': models.add_animaltype,
            '/api/weightings': models.add_weighting,
            '/api/users': models.add_user,
        }

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            handlers[path](**data)
            self._set_headers(201)
            self.wfile.write(json.dumps(
                {"message": f"{path[5:].capitalize()} добавлено успешно"}).encode('utf-8'))
        except (json.JSONDecodeError, KeyError) as e:
            self.handle_error(400, "Неверные данные JSON" if isinstance(
                e, json.JSONDecodeError) else str(e))
        except Exception as e:
            self.handle_error(500, f"Ошибка добавления: {str(e)}")

    def handle_update_animal(self, resource_id):
        self._handle_update(models.update_animal, resource_id)

    def handle_update_breed(self, resource_id):
        self._handle_update(models.update_breed, resource_id)

    def handle_update_animaltype(self, resource_id):
        self._handle_update(models.update_animaltype, resource_id)

    def handle_update_weighting(self, resource_id):
        self._handle_update(models.update_weighting, resource_id)

    def handle_update_user(self, resource_id):
        self._handle_update(models.update_user, resource_id)

    def _handle_update(self, update_function, resource_id):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)

        try:
            data = json.loads(put_data)
            update_function(int(resource_id), **data)
            self._set_headers(200)
            self.wfile.write(json.dumps(
                {"message": "Обновлено успешно"}).encode('utf-8'))
        except json.JSONDecodeError:
            self.handle_error(400, "Неверные данные JSON")
        except Exception as e:
            self.handle_error(500, f"Ошибка обновления: {str(e)}")

    def handle_auth(self, path):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            user_data = json.loads(post_data)
            auth_controller = AuthController()

            if path == '/api/register':
                status_code, response_content = auth_controller.handle_register(user_data)
            else:  # path == '/api/login'
                status_code, response_content = auth_controller.handle_login(user_data)

            self._set_headers(status_code)
            self.wfile.write(json.dumps(response_content).encode('utf-8'))
        except json.JSONDecodeError:
            self.handle_error(400, "Неверные данные JSON")

    def _show_page(self, path):
        auth_controller = AuthController()
        html_content = auth_controller.show_registration_page() if path == '/' else auth_controller.show_login_page()
        self._send_html_response(html_content)

    def handle_activate_request(self, parsed_path):
        query_params = parse_qs(parsed_path.query)
        email = query_params.get('email', [None])[0]

        if not email:
            self.handle_error(400, "Email is required")
            return

        db = connect_db()
        if db is None:
            self.handle_error(500, "Failed to connect to the database.")
            return

        cursor = db.cursor()
        try:
            status_code, response_content = activate_user(cursor, email)
            db.commit()
            self._set_headers(status_code)
            self.wfile.write(json.dumps(response_content).encode('utf-8'))
        except Exception as e:
            self.handle_error(500, f"An unexpected error occurred: {str(e)}")
        finally:
            cursor.close()
            db.close()

    def _send_html_response(self, html_content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=MainController, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
