import time
import threading
import json
import os
from lark import Lark
from interpreter.conditions import eval_condition
from interpreter.transformer import ChronoTransformer

# Name der Datei, in der wir Memory persistieren
MEMORY_FILE = "memory.json"

# Load grammar
with open("interpreter/chrono_grammar.lark") as f:
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
        # Optional: Zeige Output, falls du Debug willst
        # print(f"[info] memory.json aktualisiert: {memory}")
    except Exception as e:
        print(f"[error] Konnte {MEMORY_FILE} nicht speichern: {e}")

# Interpreter: Führt die Aktionen aus
def run_script(parsed_script):
    global memory

    # 1. Memory beim Start laden
    load_memory()

    for stmt in parsed_script:
        # 2. "set"-Statements direkt ausführen
        if stmt.get("type") == "set":
            memory[stmt["key"]] = stmt["value"]
            print(f"[set] {stmt['key']} = {stmt['value']}")
            save_memory()  # sofort in JSON schreiben
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
                                save_memory()  # sofort in JSON schreiben

                            elif typ == "wait":
                                time.sleep(act["value"])

                            elif typ == "exec":
                                code_str = val.strip('"')
                                try:
                                    exec(code_str, {}, memory)
                                except Exception as e:
                                    print(f"[exec error] {e}")

                    time.sleep(interval)
            return task

        threading.Thread(
            target=make_task(interval, condition, actions),
            daemon=True
        ).start()

    # 3. Main‐Thread aktiv halten (sonst stürzen Threads ab)
    while True:
        time.sleep(1)

# Main‐Startpunkt
if __name__ == "__main__":
    # Beispiel: Wir starten immer mit 'examples/showcase.chrono'
    with open("examples/showcase.chrono", encoding="utf-8") as f:
        code = f.read()
    tree = parser.parse(code)
    data = ChronoTransformer().transform(tree)
    run_script(data)
