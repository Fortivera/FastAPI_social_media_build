from passlib.context import CryptContext
password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hashing(password: str):
    return password.hash(password)
