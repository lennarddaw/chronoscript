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
        args = items[1] if len(items) > 1 else []
        # Rebuild the raw string version
        arg_str = ", ".join(args)
        return f"{func_name}({arg_str})"

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
