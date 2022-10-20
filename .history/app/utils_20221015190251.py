from passlib.context import CryptContext
password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hashing(password: str):
    """# this function utilizes bcrypt from passlib and .hash to hide inputed password"""
    return password_context.hash(password)
