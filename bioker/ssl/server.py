import ssl
from http.server import HTTPServer


def get_ssl_context(cert_path: str = 'server-cert.pem',
                    key_path: str = 'server-key.pem',
                    key_pass: str = 'changeme',
                    ca_path: str = None,
                    protocol: int = ssl.PROTOCOL_TLS_SERVER) -> ssl.SSLContext:
    context = ssl.SSLContext(protocol)
    context.load_cert_chain(cert_path, key_path, key_pass)
    if ca_path is not None:
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(capath=ca_path)
    return context


def wrap_http_server(context: ssl.SSLContext,
                     server: HTTPServer) -> HTTPServer:
    server.socket = context.wrap_socket(server.socket, server_side=True)
    return server
