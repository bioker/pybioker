import subprocess as s


def read_gpg_file(path: str) -> str:
    with open(path, 'r') as f:
        encrypted = f.read().encode('utf8').strip()
    decrypted = s.run(['gpg', '-q'], input=encrypted, stdout=s.PIPE).stdout.decode('utf8').strip()
    return decrypted


def write_gpg_file(content: str, path: str):
    encrypted = (s.run(['gpg', '-e', '--armor'], input=content.encode('utf8'), stdout=s.PIPE)
                 .stdout
                 .decode('utf8')
                 .strip())
    with open(path, 'w') as f:
        f.write(encrypted)
