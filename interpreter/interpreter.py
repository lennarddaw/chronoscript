import time
import threading
from lark import Lark
from interpreter.conditions import eval_condition
from interpreter.transformer import ChronoTransformer

# Load grammar
with open("interpreter/chrono_grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start")

# Global memory store
memory = {}

# Interpreter: Führt die Aktionen aus
def run_script(parsed_script):
    global memory

    for stmt in parsed_script:
        if stmt.get("type") == "set":
            memory[stmt["key"]] = stmt["value"]
            print(f"[set] {stmt['key']} = {stmt['value']}")
            continue

        if stmt.get("type") != "loop":
            continue

        interval = stmt["interval"]
        condition = stmt["condition"]
        actions = stmt["actions"]

        print(f"[debug] Parsed loop: every {interval}s if {condition} → {actions}")

        def make_task(interval, condition, actions):
            def task():
                print(f"[start] Running every {interval}s...")
                while True:
                    if eval_condition(condition, memory):
                        for act in actions:
                            typ = act.get("type")
                            val = act.get("value", "")

                            if typ == "log":
                                msg = val.strip('"')
                                print(f"[log] {msg}")

                            elif typ == "notify":
                                msg = val.strip('"')
                                print(f"[notify] {msg.upper()} 🔔")

                            elif typ == "set":
                                memory[act["key"]] = act["value"]
                                print(f"[set] {act['key']} = {act['value']}")

                            elif typ == "wait":
                                time.sleep(act["value"])

                            elif typ == "exec":
                                # val enthält den Python-Code als String, z. B. '"print(...)"'
                                code_str = val.strip('"')
                                try:
                                    # Führe code_str im Kontext von memory aus
                                    exec(code_str, {}, memory)
                                except Exception as e:
                                    print(f"[exec error] {e}")

                    time.sleep(interval)
            return task

        threading.Thread(target=make_task(interval, condition, actions), daemon=True).start()

    # Main-Thread am Leben halten
    while True:
        time.sleep(1)

# Main-Startpunkt
if __name__ == "__main__":
    with open("examples/showcase.chrono") as f:
        code = f.read()
    tree = parser.parse(code)
    data = ChronoTransformer().transform(tree)
    run_script(data)
