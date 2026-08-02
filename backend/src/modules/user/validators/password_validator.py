from zxcvbn import zxcvbn


def is_password_valid(password: str):
    result = zxcvbn(password)
    score = result["score"]
    if score >= 2:
        return True
    return False