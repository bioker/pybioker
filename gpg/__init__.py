import subprocess as s

def rgpgf(path):
    """Reads GPG encrypted file (armored)

    :param path - file path to read content from

    :type path: str

    :rtype: str
    """
    with open(path, 'r') as f:
        encrypted = f.read().encode('utf8')
    decrypted = (s
            .run(
                ['gpg', '-q'], 
                input=encrypted, 
                stdout=s.PIPE)
            .stdout.decode('utf8').strip())
    return decrypted

def wgpgf(content, path):
    """Write encrypted by GPG content (armored) to file

    :param content - content to encrypt and save
    :param path - file path to write content to

    :type content: str
    :type path: str
    """
    encrypted = (s
            .run(
                ['gpg', '-e', '--armor'], 
                input=content.encode('utf8'), 
                stdout=s.PIPE)
            .stdout.decode('utf8').strip())
    with open(path, 'w') as f:
        f.write(encrypted)
