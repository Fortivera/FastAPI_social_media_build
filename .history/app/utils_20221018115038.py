from passlib.context import CryptContext


password_contents = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_pass(password: str):
    """# this function utilizes bcrypt from passlib and .hash to hide inputed password"""
    return password_contents.hash(password)


def verify_pass(actual_pass, hashed_pass):
    return password_contents.verify(actual_pass, hashed_pass)
