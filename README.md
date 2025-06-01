# Chronoscript

**Chronoscript** ist eine kleine DSL (Domain-Specific Language) für zeit- und zustandsgesteuerte Automatisierung.  
Mit ihr kannst du in wenigen Zeilen Tasks definieren, die automatisch wiederholt, verzögert oder nur unter bestimmten Bedingungen ausgeführt werden.

---

## Inhaltsverzeichnis

1. [Projektüberblick](#projektüberblick)  
2. [Installation](#installation)  
3. [Erste Schritte & CLI](#erste-schritte--cli)  
4. [Sprachreferenz](#sprachreferenz)  
   - [`set`](#set)  
   - [`loop every … if … { … }`](#loop-every--if--)  
   - Bedingungen (`hour_between`, `random_chance`, `&&`, `||`, `!`)  
   - Aktionen: `log()`, `notify()`, `wait()`, `exec()`  
5. [Persistentes Memory (`memory.json`)](#persistentes-memory-memoryjson)  
6. [Beispielskripte](#beispielskripte)  
   - `hello.chrono`  
   - `memory.chrono`  
   - `wait.chrono`  
   - `showcase.chrono`  
7. [Troubleshooting](#troubleshooting)  
8. [Roadmap & weiterführende Ideen](#roadmap--weiterführende-ideen)

---

## Projektüberblick

Chronoscript ist eine eigenständige Language, um:

- zeitgesteuerte Schleifen zu formulieren  
- variablenbasiertes Routing („Memory“) zu betreiben  
- Aktionen wie `log`, `notify`, `wait`, `exec` auszuführen  
- Variablen persistent in einer JSON-Datei zu speichern  

Das System besteht aus:

- einer **Grammatik** (`chrono_grammar.lark`)  
- einem **Transformer** (Lark → Python-`dict`)  
- einem **Interpreter** (`interpreter.py`) mit Threads sowie Memory-Laden/-Speichern  
- einem einfachen **CLI** (`cli/run.py`)  
- mehreren **Beispielskripten** im Ordner `examples/`

---

## Installation

1. **Python 3.8+ installieren**  
2. Repository klonen:
   ```bash
   git clone https://github.com/<dein-user>/chronoscript.git
   cd chronoscript
