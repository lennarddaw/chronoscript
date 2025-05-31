import time
import re
from lark import Lark
from interpreter.conditions import eval_condition
from interpreter.transformer import ChronoTransformer

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
                    if not isinstance(act, dict):
                        return
                    typ = act.get("type")
                    val = act.get("value", "")

                    if typ == "log":
                        print(f"[log] {val}")

                    elif typ == "notify":
                        print(f"[notify] {val.upper()} 🔔")

                    elif typ == "save":
                        with open("output.log", "a", encoding="utf-8") as f:
                            f.write(f"[saved] {val}\n")
                        print(f"[save] Written to output.log")

                    elif typ == "exec":
                        try:
                            print("[exec] →", end=" ")
                            exec(val)
                        except Exception as e:
                            print(f"[exec error] {e}")

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
