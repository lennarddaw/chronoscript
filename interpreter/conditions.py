from datetime import datetime
import random

def _resolve_condition(expr: str) -> bool:
    now = datetime.now()

    if expr == "is_weekend":
        return now.weekday() >= 5
    if expr == "is_weekday":
        return now.weekday() < 5

    if expr.startswith("hour_between("):
        try:
            args = expr[13:-1].split(",")
            start = int(args[0].strip())
            end = int(args[1].strip())
            return start <= now.hour < end
        except:
            return False

    if expr.startswith("random_chance("):
        try:
            p = float(expr[15:-1])
            return random.random() < p
        except:
            return False

    if expr.startswith("date_is("):
        try:
            date_str = expr[9:-1].strip().strip('"')
            return now.strftime("%Y-%m-%d") == date_str
        except:
            return False

    return False  # fallback

def eval_condition(expr: str, memory: dict = None) -> bool:
    try:
        local_vars = {
            **{k: f'"{v}"' if isinstance(v, str) else v for k, v in (memory or {}).items()},
            "is_weekend": lambda: _resolve_condition("is_weekend"),
            "is_weekday": lambda: _resolve_condition("is_weekday"),
            "hour_between": lambda *args: _resolve_condition(f"hour_between({', '.join(map(str, args))})"),
            "date_is": lambda s: _resolve_condition(f'date_is("{s}")'),
            "random_chance": lambda p: _resolve_condition(f"random_chance({p})"),
            "true": True,
            "false": False
        }
        return eval(expr, {"__builtins__": {}}, local_vars)
    except Exception as e:
        print(f"[eval error] {e}")
        return False



