from bcrypt import checkpw, gensalt, hashpw

from .sql import db, query_db
from string import ascii_letters, digits
from random import choices

BCRYPT_HASH_FACTOR = 12

def check_passwd(email: str, password: str | bytes) -> bool:
    answer = query_db('getLogin :email', email=email)
    if not bool(answer):
        return False
    password_hash: str = answer[0][1]

    if isinstance(password, str):
        password = password.encode('ascii')
    return checkpw(password, password_hash.encode('ascii'))

def generate_hash(password: str) -> bytes:
    return hashpw(password.encode(), gensalt(BCRYPT_HASH_FACTOR))

def generate_passwd(length: int = 12) -> tuple[str, str]:
    generated_passwd = ''.join(choices(ascii_letters + digits, k=length))
    hash = generate_hash(generated_passwd).decode()
    return (generated_passwd, hash)
