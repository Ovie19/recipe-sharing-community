from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class PasswordHasher:
    def hash(self, password: str) -> str:
        return password_hash.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return password_hash.verify(password, hashed)
