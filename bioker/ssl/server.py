import socket
import ssl
from typing import Callable, Any


def get_ssl_context(cert_path: str = 'server.crt',
                    key_path: str = 'server.key',
                    key_pass: str = 'changeme',
                    protocol: int = ssl.PROTOCOL_TLS_SERVER) -> ssl.SSLContext:
    context = ssl.SSLContext(protocol)
    context.load_cert_chain(cert_path, key_path, key_pass)
    return context


def get_socket(family: int = socket.AF_INET, socket_type: int = socket.SOCK_STREAM, file_no: int = 0) -> socket.socket:
    return socket.socket(family, socket_type, file_no)


def accept(context: ssl.SSLContext,
           socket_: socket.socket = None,
           hostname: str = '0.0.0.0',
           port: int = 8443,
           handler: Callable[[Any, Any], None] = None):
    with socket_ or get_socket() as sock:
        sock.bind((hostname, port))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssl_socket:
            conn, addr = ssl_socket.accept()
            handler(conn, addr)
