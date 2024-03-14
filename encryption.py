import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from binascii import hexlify

def encrypt(text):
    algorithm = 'aes-256-cbc'
    secret = os.environ['SECRET_KEY']
    iv = get_random_bytes(16)
    cipher = AES.new(secret.encode(), AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(text.encode())
    return f'{hexlify(iv).decode()}:{hexlify(encrypted).decode()}'


def decrypt(ciphertext):
    algorithm = 'aes-256-cbc'
    secret = os.environ['SECRET_KEY']
    iv, encrypted = ciphertext.split(':')
    cipher = AES.new(secret.encode(), AES.MODE_CBC, bytes.fromhex(iv))
    decrypted = cipher.decrypt(bytes.fromhex(encrypted))
    return decrypted.decode()