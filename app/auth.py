from bcrypt import checkpw, gensalt, hashpw

from .sql import db, execute_on_db
from string import ascii_letters, digits
from random import choices

BCRYPT_HASH_FACTOR = 12

def check_passwd(email: str, password: str | bytes) -> bool:
    #FIXME - sanitize input
    cursor = db.cursor()
    response = cursor.execute(f"getLogin '{email}'")
    answer = response.fetchone()
    if answer is None:
        return False
    password_hash: str = answer[1]

    if isinstance(password, str):
        password = password.encode('ascii')
    return checkpw(password, password_hash.encode('ascii'))

def generate_hash(password: str) -> bytes:
    return hashpw(password.encode(), gensalt(BCRYPT_HASH_FACTOR))

def generate_passwd(length: int = 12) -> str:
    return ''.join(choices(ascii_letters + digits, k=length))