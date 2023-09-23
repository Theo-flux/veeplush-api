from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_pwd_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)
