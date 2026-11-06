from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = 8000
TEMPLATE_PATH = os.path.join("web", "index.html")


class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Проверяем, запрашивает ли браузер статический файл (CSS или JS)
        if self.path.startswith("/static/"):
            # Превращаем URL-путь в реальный путь к файлу на диске (убираем первый слэш)
            file_path = self.path.lstrip("/")

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)

                # Задаем правильный Content-type в зависимости от расширения файла
                if file_path.endswith(".css"):
                    self.send_header("Content-type", "text/css")
                elif file_path.endswith(".js"):
                    self.send_header("Content-type", "application/javascript")

                self.end_headers()

                # Читаем и отправляем файл (стили или скрипт)
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                # Если файл в папке static не найден
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Static file not found")
                return

        # 2. На ЛЮБОЙ другой запрос отдаем index.html
        if os.path.exists(TEMPLATE_PATH):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open(TEMPLATE_PATH, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>Error 404: templates/index.html not found!</h1>")


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
