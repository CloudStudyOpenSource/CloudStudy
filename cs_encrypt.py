import hashlib


def sha1(input):
    input = hashlib.sha1(input.encode('utf-8'))
    return input.hexdigest()


def sha512(input):
    input = hashlib.sha512(input.encode('utf-8'))
    return input.hexdigest()
