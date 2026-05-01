from functools import lru_cache
from pwdlib import PasswordHash


@lru_cache
def get_password_hash():
    return PasswordHash.recommended()
