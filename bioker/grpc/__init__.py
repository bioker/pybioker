import subprocess as sub
from sys import path


def generate_from_proto(path_to_find: str, output_path: str, exclude: str = 'build') -> sub.CompletedProcess:
    """Generate Python gRPC files from proto files found in specified directory

    :param path_to_find - path where to find proto files 
        (recursive search with find command)
    :param output_path - path where generated python source files will be placed
        (also this path will be added to sys.path to be able import 
        generated files)
    :param exclude - grep pattern to exclude proto files
    """
    pre_result = sub.run(['find', path_to_find, '-name', '*.proto'],
                         stdout=sub.PIPE)
    filtered_result = sub.run(['grep', '-v', exclude],
                              input=pre_result.stdout, stdout=sub.PIPE)
    files = (filtered_result
             .stdout
             .decode('utf8')
             .strip()
             .split('\n'))
    dirs = set(map(lambda f: f[:f.rfind('/')], files))
    output = sub.run(['python3', '-m', 'grpc_tools.protoc']
                     + list(map(lambda d: '-I' + d, dirs))
                     + ['--python_out', output_path]
                     + ['--grpc_python_out', output_path]
                     + files, stdout=sub.PIPE)
    path.append(output_path)
    return output
