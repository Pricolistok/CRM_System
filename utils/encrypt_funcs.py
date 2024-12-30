from passlib.context import CryptContext
from settings.encrypt_settings import ALPHABET, LEN_ALPHABET


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_eq_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_pwd(text: str) -> str:
    return pwd_context.hash(text)


def encrypt_text(data: str, level_encrypt: int):
    for cnt_level_encrypt in range(level_encrypt):
        encrypt_data = ''
        for elem_in_data in data:
            index = ALPHABET.index(elem_in_data)
            if index > LEN_ALPHABET - 4:
                encrypt_data += ALPHABET[index - LEN_ALPHABET + 3]
            else:
                encrypt_data += ALPHABET[index + 3]
        data = encrypt_data
    return data


def decode_text(data: str, level_decode: int):
    for cnt_level_decode in range(level_decode):
        decode_data = ''
        for elem_in_data in data:
            index = ALPHABET.index(elem_in_data)
            if index < 0:
                decode_data += ALPHABET[LEN_ALPHABET - index + 3]
            else:
                decode_data += ALPHABET[index - 3]
        data = decode_data
    return data