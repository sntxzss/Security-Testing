from pwdlib import PasswordHash

ph = PasswordHash.recommended()

def hash_password(password:str) -> str:
    return ph.hash(password)

def password_verify(password:str, hashed:str) -> bool:
    return ph.verify(password, hashed)