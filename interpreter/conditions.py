from datetime import datetime

def eval_condition(name: str) -> bool:
    if name == "true":
        return True
    if name == "false":
        return False
    if name.startswith("is_weekend"):
        return datetime.now().weekday() >= 5
    return False
