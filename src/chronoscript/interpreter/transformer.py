from lark import Transformer, Token


class ChronoTransformer(Transformer):
    # -------------------------------
    # Literale
    # -------------------------------
    def number(self, items):
        # items[0] ist ein Token("NUMBER", "123")
        return int(items[0])

    def string(self, items):
        # items[0] ist ein Token("ESCAPED_STRING", "\"Hello\"")
        text = items[0][1:-1]  # Entferne die äußeren Anführungszeichen
        return text

    def true(self, _):
        return True

    def false(self, _):
        return False

    def var(self, items):
        # items[0] ist ein Token("CNAME", "variableName")
        return {"type": "var", "value": str(items[0])}

    # -------------------------------
    # Arithmetik und Vergleich
    # -------------------------------
    def add(self, items):
        return {"type": "add", "left": items[0], "right": items[1]}

    def sub(self, items):
        return {"type": "sub", "left": items[0], "right": items[1]}

    def mul(self, items):
        return {"type": "mul", "left": items[0], "right": items[1]}

    def div(self, items):
        return {"type": "div", "left": items[0], "right": items[1]}

    def mod(self, items):
        return {"type": "mod", "left": items[0], "right": items[1]}

    def neg(self, items):
        return {"type": "neg", "value": items[0]}

    def comparison(self, items):
        # items können [leftExpr] oder [leftExpr, opToken, rightExpr]
        if len(items) == 1:
            return items[0]
        left, op_token, right = items
        op = str(op_token)
        return {"type": "cmp", "op": op, "left": left, "right": right}

    def and_expr(self, items):
        return {"type": "and", "left": items[0], "right": items[1]}

    def or_expr(self, items):
        return {"type": "or", "left": items[0], "right": items[1]}

    def not_expr(self, items):
        return {"type": "not", "value": items[0]}

    # -------------------------------
    # Funktionsaufruf in Expressions
    # -------------------------------
    def func_call(self, items):
        # items[0] ist Token("CNAME", functionName)
        # items[1] ist ggf. eine Liste von Argumenten
        name = str(items[0])
        raw_args = items[1] if len(items) > 1 else []
        if not isinstance(raw_args, list):
            raw_args = [raw_args]
        return {"type": "call_expr", "name": name, "args": raw_args}

    def arg_list(self, items):
        return items

    # -------------------------------
    # Funktionsdefinition (optional)
    # -------------------------------
    def fn_def(self, items):
        # items: [Token("CNAME", fnName), [param_list], statement...]
        fn_name = str(items[0])
        params = items[1] if isinstance(items[1], list) else []
        body = items[2:]
        return {"type": "fn_def", "name": fn_name, "params": params, "body": body}

    def param_list(self, items):
        return [str(tok) for tok in items]

    # -------------------------------
    # Actions: call, set, wait, dump
    # -------------------------------
    def call(self, items):
        # items: [Token("CNAME", actionName), either string or exprTree]
        name = str(items[0])
        val = items[1]
        return {"type": name, "value": val}

    def dump(self, _):
        return {"type": "dump"}

    def set(self, items):
        # items: [Token("CNAME", varName), exprTree or NUMBER or ESCAPED_STRING]
        key = str(items[0])
        raw = items[1]

        # Wenn raw ein NUMBER-Token ist, konvertiere zu int
        if isinstance(raw, Token) and raw.type == "NUMBER":
            val = int(raw)
        else:
            # raw kann ein String, ein var-Dict oder ein Expression-Tree sein
            # Wenn raw ist ein Token("ESCAPED_STRING", "\"text\""), entferne Anführungszeichen
            if isinstance(raw, Token) and raw.type == "ESCAPED_STRING":
                temp = str(raw)
                val = temp[1:-1]
            else:
                val = raw
        return {"type": "set", "key": key, "value": val}

    def wait(self, items):
        # items[0] ist TIME in Sekunden (int)
        return {"type": "wait", "value": items[0]}

    def action(self, items):
        # items[0] ist bereits ein Dict von call, set, wait oder dump
        return items[0]

    # -------------------------------
    # Statement & Start
    # -------------------------------
    def statement(self, items):
        # items kann sein:
        # - [loopInterval, conditionExpr, actionDict...]
        # - oder eine fn_def-Dict direkt
        first = items[0]
        if isinstance(first, dict) and first.get("type") == "fn_def":
            return first
        interval = items[0]
        condition = items[1]
        actions = items[2:]
        return {"type": "loop", "interval": interval, "condition": condition, "actions": actions}

    def start(self, items):
        return items
