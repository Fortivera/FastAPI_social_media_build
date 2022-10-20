from passlib.context import CryptContext
password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# this function utilizes bcrypt from passlib and .hash to hide inputed password


def hashing(password: str):
    return password_context.hash(password)
