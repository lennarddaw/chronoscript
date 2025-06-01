from lark import Transformer

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

        if not isinstance(raw_args, list):
            raw_args = [raw_args]

        args = [str(arg) if arg is not None else "" for arg in raw_args]
        arg_str = ", ".join(args)
        return f"{func_name}({arg_str})"

    def or_expr(self, items):
        return f"({items[0]}) or ({items[1]})"

    def and_expr(self, items):
        return f"({items[0]}) and ({items[1]})"

    def not_expr(self, items):
        return f"not ({items[0]})"

    # --- Action-Handler: call, set, wait ---

    def call(self, items):
        # items = [CNAME, optional ESCAPED_STRING]
        name = str(items[0])
        val = str(items[1]) if len(items) > 1 else ""
        return {"type": name, "value": val}

    def set(self, items):
        # items = [CNAME, valueToken/CNAME]
        key = str(items[0])
        val = str(items[1])
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        return {"type": "set", "key": key, "value": val}

    def wait(self, items):
        # items[0] ist eine Zeit in Sekunden (int), weil TIME schon konvertiert
        return {"type": "wait", "value": items[0]}

    def action(self, items):
        # Hier wird das einzelne Dict, das von call/set/wait zurückkam, einfach weitergereicht
        return items[0]

    # --- Rest: Statement & Start ---

    def raw_condition(self, items):
        return str(items[0]).strip()

    def statement(self, items):
        return {
            "type": "loop",
            "interval": items[0],
            "condition": items[1],
            "actions": items[2:]
        }

    def start(self, items):
        return items
