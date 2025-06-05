import re

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False

    email_regex = re.compile(
        r"^[A-Za-z0-9._%+\-]+@"       
        r"[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
    )

    return bool(email_regex.match(email))