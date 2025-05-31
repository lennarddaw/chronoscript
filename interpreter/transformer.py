
from lark import Transformer

class ChronoTransformer(Transformer):
    def TIME(self, token):
        value = int(token[:-1])
        unit = token[-1]
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
        return value * multiplier

    def condition(self, items):
        return str(items[0])

    def action(self, items):
        return str(items[0]).strip()

    def statement(self, items):
        return {
            "interval": items[0],
            "condition": items[1],
            "actions": items[2:]
        }

    def start(self, items):
        return items
