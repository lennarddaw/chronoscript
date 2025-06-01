import time
import threading
import json
import os
import random
from datetime import datetime
from lark import Lark
from chronoscript.interpreter.parser import parser
from chronoscript.interpreter.transformer import ChronoTransformer

# Name der Datei, in der wir Memory persistieren
MEMORY_FILE = os.getenv("CHRONO_MEMORY_FILE", "memory.json")

# Load grammar
BASE_DIR = os.path.dirname(__file__)
GRAMMAR_PATH = os.path.join(BASE_DIR, "chrono_grammar.lark")
with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
    grammar = f.read()

parser = Lark(grammar, start="start")

# Globales Memory‐Dict (wird beim Start aus memory.json gefüllt)
memory = {}


def load_memory():
    """Lädt memory.json, falls vorhanden, sonst bleibt memory leer."""
    global memory
    if os.path.isfile(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
            print(f"[info] Loaded memory from {MEMORY_FILE}: {memory}")
        except Exception as e:
            print(f"[warn] Konnte {MEMORY_FILE} nicht laden: {e}")
            memory = {}
    else:
        memory = {}


def save_memory():
    """Schreibt das aktuelle Memory‐Dict in memory.json."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[error] Konnte {MEMORY_FILE} nicht speichern: {e}")


def eval_expr(node, memory):
    """
    Rekursive Auswertung eines Expression-Tree-Nodes.
    node kann sein:
      - int, bool, str: Literal-Wert
      - {'type': 'var', 'value': varname}
      - {'type': 'add'|'sub'|'mul'|'div'|'mod', 'left':..., 'right':...}
      - {'type': 'neg', 'value': ...}
      - {'type': 'cmp', 'op': '=='|... , 'left':..., 'right':...}
      - {'type': 'and'|'or', 'left':..., 'right':...}
      - {'type': 'not', 'value': ...}
      - {'type': 'call_expr', 'name': fnName, 'args': [argExprs]}
    """
    # 1. Primitive Literale
    if isinstance(node, (int, bool, str)):
        return node

    # 2. Variablezugriff
    if isinstance(node, dict) and node.get("type") == "var":
        varname = node["value"]
        return memory.get(varname)

    # 3. Arithmetik
    typ = node.get("type")
    if typ in ("add", "sub", "mul", "div", "mod"):
        left = eval_expr(node["left"], memory)
        right = eval_expr(node["right"], memory)
        if typ == "add":
            return left + right
        if typ == "sub":
            return left - right
        if typ == "mul":
            return left * right
        if typ == "div":
            return left // right
        if typ == "mod":
            return left % right

    # 4. Negation
    if typ == "neg":
        return -eval_expr(node["value"], memory)

    # 5. Vergleich
    if typ == "cmp":
        left = eval_expr(node["left"], memory)
        right = eval_expr(node["right"], memory)
        op = node["op"]
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right

    # 6. Boolesche Verknüpfung
    if typ == "and":
        return eval_expr(node["left"], memory) and eval_expr(node["right"], memory)
    if typ == "or":
        return eval_expr(node["left"], memory) or eval_expr(node["right"], memory)
    if typ == "not":
        return not eval_expr(node["value"], memory)

    # 7. Funktionsaufruf (built-in)
    if typ == "call_expr":
        fn_name = node["name"]
        args = [eval_expr(arg, memory) for arg in node["args"]]
        if fn_name == "hour_between":
            start, end = args
            now = datetime.now()
            return start <= now.hour < end
        if fn_name == "date_is":
            target = args[0]
            return datetime.now().strftime("%Y-%m-%d") == target
        if fn_name == "random_chance":
            p = float(args[0])
            return random.random() < p
        # Weitere built-ins:
        if fn_name == "abs":
            return abs(args[0])
        if fn_name == "max":
            return max(*args)
        if fn_name == "min":
            return min(*args)
        # Unbekannte Funktion: None zurückgeben
        return None

    # Fallback
    return None


def run_script(parsed_script):
    global memory

    # 1. Memory beim Start laden
    load_memory()

    for stmt in parsed_script:
        # 2. "set"-Statements direkt ausführen (Top-Level)
        if stmt.get("type") == "set":
            new_val = stmt["value"]
            # Wenn new_val ein Expression-Tree ist, auswerten:
            if isinstance(new_val, dict) or isinstance(new_val, (int, bool, str)):
                result = eval_expr(new_val, memory)
            else:
                result = new_val
            memory[stmt["key"]] = result
            print(f"[set] {stmt['key']} = {result}")
            save_memory()
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
                    cond_val = eval_expr(condition, memory)
                    if cond_val:
                        for act in actions:
                            typ = act.get("type")
                            val = act.get("value", "")

                            if typ == "log":
                                msg_val = eval_expr(val, memory)
                                print(f"[log] {msg_val}")

                            elif typ == "notify":
                                msg_val = eval_expr(val, memory)
                                print(f"[notify] {msg_val.upper()} 🔔")

                            elif typ == "set":
                                raw_val = act["value"]
                                new_val = eval_expr(raw_val, memory)
                                memory[act["key"]] = new_val
                                print(f"[set] {act['key']} = {new_val}")
                                save_memory()

                            elif typ == "wait":
                                time.sleep(act["value"])

                            elif typ == "exec":
                                code_str = eval_expr(val, memory)
                                try:
                                    exec(code_str, {}, memory)
                                except Exception as e:
                                    print(f"[exec error] {e}")

                            elif typ == "dump":
                                print("[dump_memory] Current memory:")
                                for key, value in memory.items():
                                    print(f"  {key}: {value}")
                                try:
                                    with open("memory_dump.json", "w", encoding="utf-8") as f:
                                        json.dump(memory, f, ensure_ascii=False, indent=2)
                                    print("[dump_memory] Wrote memory_dump.json")
                                except Exception as e:
                                    print(f"[dump_memory error] {e}")

                    time.sleep(interval)

            return task

        threading.Thread(
            target=make_task(interval, condition, actions),
            daemon=True
        ).start()

    # 3. Main‐Thread am Leben halten
    while True:
        time.sleep(1)


# Main‐Startpunkt
if __name__ == "__main__":
    # Beispiel: Wir starten immer mit 'examples/showcase.chrono'
    script_path = os.path.join(os.path.dirname(__file__), "..", "examples", "showcase.chrono")
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(code)
    data = ChronoTransformer().transform(tree)
    run_script(data)
