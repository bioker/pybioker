import subprocess as sub
from sys import path
from typing import List


def generate_from_proto(files: List[str], output_path: str) -> sub.CompletedProcess:
    dirs = set(map(lambda f: f[:f.rfind('/')], files))
    output = sub.run(['python3', '-m', 'grpc_tools.protoc']
                     + list(map(lambda d: '-I' + d, dirs))
                     + ['--python_out', output_path]
                     + ['--grpc_python_out', output_path]
                     + files, stdout=sub.PIPE)
    path.append(output_path)
    return output
