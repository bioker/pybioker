import requests as req

client_cert = '/home/wls/test/client-cert.pem'
client_key = '/home/wls/test/client-key.pem'
url = 'https://localhost:8080'
ca_cert = '/home/wls/test/ca-cert.pem'

print(req.get(url, cert=(client_cert, client_key), verify=ca_cert).text)
