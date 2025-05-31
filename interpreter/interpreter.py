import time
import re
from lark import Lark, Transformer

# Load grammar
with open("interpreter/chrono_grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start")

# Transformer: Wandelt Parse-Tree in brauchbare Datenstrukturen
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

# Interpreter: Führt die Aktionen aus
def run_script(parsed_script):
    for stmt in parsed_script:
        interval = stmt["interval"]
        condition = stmt["condition"]
        actions = stmt["actions"]

        def task():
            if condition == "true":  # Platzhalter für echte Eval-Logik
                for act in actions:
                    if act.startswith("log("):
                        msg = re.findall(r'"(.*?)"', act)
                        print(f"[log] {msg[0] if msg else ''}")
        
        # Zeitgesteuerte Ausführung – nur einmal für Demo
        print(f"[start] Running every {interval}s...")
        task()
        while True:
            time.sleep(interval)
            task()

# Main
if __name__ == "__main__":
    with open("examples/hello.chrono") as f:
        code = f.read()
    tree = parser.parse(code)
    data = ChronoTransformer().transform(tree)
    run_script(data)
