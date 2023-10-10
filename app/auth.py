import bcrypt
from .sql import db

def check_passwd(password: str | bytes) -> bool:
    cursor = db.cursor()
    response = cursor.execute("getLogin 'admin@sms.com'")
    answer = response.fetchone()
    if type(password) == str:
        password = password.encode('ascii')
    if answer:
        return bcrypt.checkpw(password, answer[1])
    return False