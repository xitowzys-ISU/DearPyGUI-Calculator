import string


def safe_eval(exprs: str) -> tuple[str, bool]:

    if exprs == "":
        return "0", False
    if exprs in string.ascii_letters:
        return "0", False
    try:
        return str(eval(exprs)), True
    except Exception as e:
        print(str(e))
        return "0", False
