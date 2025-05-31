import time
import re
from lark import Lark
from interpreter.conditions import eval_condition
from interpreter.transformer import ChronoTransformer  # <-- falls Transformer ausgelagert

# Load grammar
with open("interpreter/chrono_grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start")

# Interpreter: Führt die Aktionen aus
def run_script(parsed_script):
    for stmt in parsed_script:
        interval = stmt["interval"]
        condition = stmt["condition"]
        actions = stmt["actions"]

        def task():
            if eval_condition(condition):
                for act in actions:
                    if isinstance(act, dict) and act.get("type") == "log":
                        print(f"[log] {act.get('value', '')}")

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
