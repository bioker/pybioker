from bioker.http.server import get_http_server
from bioker.ssl.server import get_ssl_context
from bioker.ssl.server import wrap_http_server

ssl_context = get_ssl_context(cert_path='/home/wls/test/server-cert.pem',
                              key_path='/home/wls/test/server-key.pem',
                              ca_path='/home/wls/test/test.pem')
server = wrap_http_server(ssl_context, get_http_server())

server.serve_forever()
