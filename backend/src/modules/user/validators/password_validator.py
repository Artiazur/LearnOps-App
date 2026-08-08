from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1,
)

def is_password_valid(password: str) -> bool:
    return len(policy.test(password)) == 0