from lark import Transformer, Tree, Token

class ChronoTransformer(Transformer):
    def TIME(self, token):
        value = int(token[:-1])
        unit = token[-1]
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
        return value * multiplier

    def simple_cond(self, items):
        return str(items[0])

    def condition_arg(self, items):
        return str(items[0])

    def condition_args(self, items):
        return [str(i) for i in items]
    
    def func_call(self, items):
        func_name = str(items[0])
        raw_args = items[1] if len(items) > 1 else []

        # Falls nur ein Argument ohne Liste übergeben wurde
        if not isinstance(raw_args, list):
            raw_args = [raw_args]

        # Konvertiere alle Argumente sicher zu String
        args = [str(arg) if arg is not None else "" for arg in raw_args]

        arg_str = ", ".join(args)
        return f"{func_name}({arg_str})"


    def or_expr(self, items):
        return f"({items[0]}) or ({items[1]})"

    def and_expr(self, items):
        return f"({items[0]}) and ({items[1]})"

    def not_expr(self, items):
        return f"not ({items[0]})"


    def string(self, items):
        return str(items[0])[1:-1]  # Strip quotes

    def action(self, items):
        name = str(items[0])
        value = items[1] if len(items) > 1 else ""
        return {"type": name, "value": value}

    def statement(self, items):
        return {
            "interval": items[0],
            "condition": items[1],
            "actions": items[2:]
        }

    def start(self, items):
        return items
