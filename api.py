import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from auth_controller import AuthController
from activate import activate_user
from models import (
    get_users, get_animals, get_animaltypes,
    get_breeds, get_weightings,
    add_animal, update_animal, delete_animal,
    add_animaltype, update_animaltype, delete_animaltype,
    add_breed, update_breed, delete_breed,
    add_weighting, update_weighting, delete_weighting
)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        handlers = {
            '/': self._show_registration_page,
            '/login': self._show_login_page,
            '/users': self._get_users,
            '/animals': self._get_animals,
            '/animaltypes': self._get_animaltypes,
            '/breeds': self._get_breeds,
            '/weightings': self._get_weightings,
        }

        handler = handlers.get(path)
        if handler:
            handler()
        elif path.startswith('/activate'):
            self.handle_activate_request(urlparse(self.path))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        handlers = {
            '/register': self.handle_register,
            '/login': self.handle_login,
            '/animals': self.handle_add_animal,
            '/animaltypes': self.handle_add_animaltype,
            '/breeds': self.handle_add_breed,
            '/weightings': self.handle_add_weighting,
        }

        handler = handlers.get(path)
        if handler:
            handler()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        path = urlparse(self.path).path
        id_mapping = {
            '/animals/': self.handle_update_animal,
            '/animaltypes/': self.handle_update_animaltype,
            '/breeds/': self.handle_update_breed,
            '/weightings/': self.handle_update_weighting,
        }

        for prefix, handler in id_mapping.items():
            item_id = self._get_id_from_path(path, prefix)
            if item_id is not None:
                handler(item_id)
                return

        self.send_response(404)
        self.end_headers()

    def do_DELETE(self):
        path = urlparse(self.path).path
        id_mapping = {
            '/animals/': self.handle_delete_animal,
            '/animaltypes/': self.handle_delete_animaltype,
            '/breeds/': self.handle_delete_breed,
            '/weightings/': self.handle_delete_weighting,
        }

        for prefix, handler in id_mapping.items():
            item_id = self._get_id_from_path(path, prefix)
            if item_id is not None:
                handler(item_id)
                return

        self.send_response(404)
        self.end_headers()

    def _show_registration_page(self):
        auth_controller = AuthController()
        self._send_html_response(auth_controller.show_registration_page())

    def _show_login_page(self):
        auth_controller = AuthController()
        self._send_html_response(auth_controller.show_login_page())

    def handle_activate_request(self, parsed_path):
        email = parse_qs(parsed_path.query).get('email', [None])[0]
        if not email:
            self._send_response(400, {"error": "Email is required"})
            return

        self._db_operation(lambda cursor: activate_user(cursor, email))

    def handle_login(self):
        auth_controller = AuthController()
        self._handle_request(auth_controller.handle_login)

    def handle_register(self):
        auth_controller = AuthController()
        self._handle_request(auth_controller.handle_register)

    def handle_add_animal(self):
        self._handle_add_data(add_animal)

    def handle_update_animal(self, animal_id):
        self._handle_update_data(update_animal, animal_id)

    def handle_delete_animal(self, animal_id):
        self._handle_delete_data(delete_animal, animal_id)

    def handle_add_animaltype(self):
        self._handle_add_data(add_animaltype)

    def handle_update_animaltype(self, animaltype_id):
        self._handle_update_data(update_animaltype, animaltype_id)

    def handle_delete_animaltype(self, animaltype_id):
        self._handle_delete_data(delete_animaltype, animaltype_id)

    def handle_add_breed(self):
        self._handle_add_data(add_breed)

    def handle_update_breed(self, breed_id):
        self._handle_update_data(update_breed, breed_id)

    def handle_delete_breed(self, breed_id):
        self._handle_delete_data(delete_breed, breed_id)

    def handle_add_weighting(self):
        self._handle_add_data(add_weighting)

    def handle_update_weighting(self, weighting_id):
        self._handle_update_data(update_weighting, weighting_id)

    def handle_delete_weighting(self, weighting_id):
        self._handle_delete_data(delete_weighting, weighting_id)

    def _handle_request(self, handler_function):
        try:
            post_data = self._get_post_data()
            if not post_data:
                self._send_response(400, {"error": "Empty request body"})
                return

            status_code, response_content = handler_function(post_data)
            self._send_response(status_code, response_content)
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
        except Exception as e:
            self._send_response(500, {"error": f"An unexpected error occurred: {str(e)}"})

    def _handle_add_data(self, add_function):
        post_data = self._get_post_data()
        if post_data:
            try:
                data = json.loads(post_data)
                add_function(**data)  
                self._send_response(201, {"message": "Data added successfully"})
            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON"})
            except Exception as e:
                self._send_response(500, {"error": f"An unexpected error occurred: {str(e)}"})

    def _handle_update_data(self, update_function, item_id):
        post_data = self._get_post_data()
        if post_data:
            try:
                data = json.loads(post_data)
                update_function(item_id, **data)
                self._send_response(200, {"message": "Data updated successfully"})
            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON"})
            except Exception as e:
                self._send_response(500, {"error": f"An unexpected error occurred: {str(e)}"})

    def _handle_delete_data(self, delete_function, item_id):
        try:
            delete_function(item_id)
            self._send_response(200, {"message": "Data deleted successfully"})
        except Exception as e:
            self._send_response(500, {"error": f"An unexpected error occurred: {str(e)}"})

    def _get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        return self.rfile.read(content_length).decode('utf-8') if content_length else None

    def _send_response(self, status_code, response_content):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response_content, ensure_ascii=False).encode('utf-8'))

    def _send_html_response(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def _get_id_from_path(self, path, prefix):
        return path[len(prefix):] if path.startswith(prefix) else None

    def _get_users(self):
        self._send_response(200, {"users": get_users()})

    def _get_animals(self):
        self._send_response(200, {"animals": get_animals()})

    def _get_animaltypes(self):
        self._send_response(200, {"animal_types": get_animaltypes()})

    def _get_breeds(self):
        self._send_response(200, {"breeds": get_breeds()})

    def _get_weightings(self):
        self._send_response(200, {"weightings": get_weightings()})

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
