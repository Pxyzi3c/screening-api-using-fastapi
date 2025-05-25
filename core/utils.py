import re

def standardize_name(name: str) -> str:
    name = re.sub(r"[/-]", " ", name).upper()
    name = re.sub(r"[^A-Z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def get_full_name(fname: str, lname: str) -> str:
    return f"{fname.title()} {lname.title()}"