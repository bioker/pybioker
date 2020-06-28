from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler


def get_http_server(hostname: str = '0.0.0.0',
                    port: int = 8080,
                    handler: BaseHTTPRequestHandler = SimpleHTTPRequestHandler):
    return HTTPServer((hostname, port), handler)
