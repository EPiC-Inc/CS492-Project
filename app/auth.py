from bcrypt import checkpw, gensalt, hashpw

from .sql import db


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

    return False

def generate_hash(password: str) -> bytes:
    return hashpw(password.encode(), gensalt(BCRYPT_HASH_FACTOR))