from datetime import datetime
import random

def eval_condition(expr: str) -> bool:
    now = datetime.now()

    # Fixe Bedingungen
    if expr == "true":
        return True
    if expr == "false":
        return False
    if expr.startswith("is_weekend"):
        return now.weekday() >= 5
    if expr.startswith("is_weekday"):
        return now.weekday() < 5

    # hour_between(x, y)
    if expr.startswith("hour_between("):
        try:
            args = expr[13:-1].split(",")
            start = int(args[0].strip())
            end = int(args[1].strip())
            return start <= now.hour < end
        except:
            return False

    # date_is("YYYY-MM-DD")
    if expr.startswith("date_is("):
        try:
            date_str = expr[9:-2]
            return now.strftime("%Y-%m-%d") == date_str
        except:
            return False

    # random_chance(0.2)
    if expr.startswith("random_chance("):
        try:
            prob = float(expr[15:-1])
            return random.random() < prob
        except:
            return False

    return False  # Default: unknown condition
