import subprocess as s
from pathlib import Path
from typing import Union, Dict


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


def read_gpg_dir(directory_path: str) -> Dict[str, Union[str, dict]]:
    result = {}
    dir_path = Path(directory_path)
    for sub_path in dir_path.iterdir():
        if sub_path.is_dir():
            result[sub_path.name] = read_gpg_dir(str(sub_path))
        elif sub_path.is_file():
            result[sub_path.name] = read_gpg_file(str(sub_path))
    return result
