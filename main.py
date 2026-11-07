from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = 8000
TEMPLATE_PATH = os.path.join("web", "index.html")
ERR_404_PATH = os.path.join("web", "404.html")
ERR_500_PATH = os.path.join("web", "500.html")


class CustomHandler(BaseHTTPRequestHandler):
    def send_error_page(self, status_code, filepath, default_message):
        """Вспомогательный метод для отправки HTML-страницы ошибки."""
        self.send_response(status_code)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        else:
            # Запасной вариант, если сам HTML-файл ошибки не найден
            self.wfile.write(default_message.encode('utf-8'))

    def do_GET(self):
        try:
            if self.path.startswith("/static/"):
                file_path = self.path.lstrip("/")

                if os.path.exists(file_path) and os.path.isfile(file_path):
                    self.send_response(200)

                    # Задаем правильный Content-type
                    if file_path.endswith(".css"):
                        self.send_header("Content-type", "text/css")
                    elif file_path.endswith(".js"):
                        self.send_header("Content-type", "application/javascript")

                    self.end_headers()

                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())
                    return
                else:
                    # Ошибка 404 для статического файла
                    self.send_error_page(404, ERR_404_PATH, "<h1>404: Статический файл не найден</h1>")
                    return

            # 2. На ЛЮБОЙ другой запрос отдаем index.html
            if self.path == "/":
                if os.path.exists(TEMPLATE_PATH):
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    with open(TEMPLATE_PATH, "rb") as f:
                        self.wfile.write(f.read())
                    return
                else:
                    self.send_error_page(404, ERR_404_PATH, "<h1>Error 404: index.html не найден!</h1>")
                    return

                # 3. Если путь не "/" и не существующий статический файл — это 404 Ошибка
            self.send_error_page(404, ERR_404_PATH, "<h1>Error 404: Страница не найдена!</h1>")

        except Exception as e:
            # Ловим любые непредвиденные сбои (ошибка 500)
            print(f"[ERROR] Ошибка сервера: {e}")
            self.send_error_page(500, ERR_500_PATH, f"<h1>Error 500: Внутренняя ошибка сервера</h1>")


def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"Сервер запущен на http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")


if __name__ == "__main__":
    run()
