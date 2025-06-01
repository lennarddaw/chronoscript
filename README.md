# Chronoscript

**Chronoscript** ist eine kleine DSL für zeit- und zustandsgesteuerte Automatisierung.  
Mit ihr kannst du in wenigen Zeilen Tasks definieren, die automatisch wiederholt, verzögert oder nur unter bestimmten Bedingungen ausgeführt werden.

---

## Inhaltsverzeichnis

1. [Projektüberblick](#projektüberblick)  
2. [Installation](#installation)  
3. [Erste Schritte & CLI](#erste-schritte--cli)  
4. [Sprachreferenz](#sprachreferenz)  
   - `set`  
   - `loop every … if … { … }`  
   - Bedingungen (`hour_between`, `random_chance`, `&&`, `||`, `!`)  
   - Aktionen: `log()`, `notify()`, `wait()`, `exec()`  
5. [Persistentes Memory (`memory.json`)](#persistentes-memory-memoryjson)  
6. [Beispielskripte](#beispielskripte)  
   - `hello.chrono`  
   - `memory.chrono`  
   - `showcase.chrono`  
7. [Troubleshooting](#troubleshooting)  
8. [Roadmap & weiterführende Ideen](#roadmap--weiterführende-ideen)

---

## Projektüberblick

Chronoscript ist eine eigenständige Language, um…

- …zeitgesteuerte Schleifen zu formulieren  
- …variablenbasiertes Routing („Memory“) zu betreiben  
- …Aktionen wie `log`, `notify`, `wait`, `exec` auszuführen  
- …Variablen persistent in einer JSON-Datei zu speichern  

Das System besteht aus:

- einer **Grammatik** (`chrono_grammar.lark`)  
- einem **Transformer** (Lark → Python-Dicts)  
- einem **Interpreter** (`interpreter.py`) mit Threads, Memory-Laden/-Speichern  
- einem einfachen **CLI** (`cli/run.py`)  
- mehreren **Beispielskripten** im Ordner `examples/`

---

## Installation

1. Stelle sicher, dass Python 3.8+ installiert ist.  
2. Klone das Repository:
   ```bash
   git clone https://github.com/<dein-user>/chronoscript.git
   cd chronoscript
(Optional) Erstelle und aktiviere ein virtuelles Environment:

bash
Kopieren
Bearbeiten
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Installiere die Abhängigkeiten (Lark):

bash
Kopieren
Bearbeiten
pip install lark-parser
Erste Schritte & CLI
In deinem Projektordner findest du den Ordner examples/ mit einigen Demo-Skripten:

hello.chrono

memory.chrono

wait.chrono

showcase.chrono

Führe ein beliebiges Beispiel so aus:

bash
Kopieren
Bearbeiten
py cli/run.py examples/hello.chrono
Das lädt die Grammatik, parst das Skript, transformiert es in Python-Daten und startet den Interpreter.

Sprachreferenz
set
Weist eine Variable zu und speichert sie im Memory (JSON).

chrono
Kopieren
Bearbeiten
set mood = "tired";
set counter = 5;
loop every <TIME> if <condition> { <action>+ }
Wiederholt den Block alle <TIME> Sekunden, wenn <condition> wahr ist.

<TIME>: Zahl + Einheit (s/m/h/d), z. B. 5s, 2m, 1h.

<condition>: Beliebiger Python-auswertbarer Ausdruck, z. B. true, random_chance(0.3), hour_between(9,17) && mood == "tired".

<action>: Eine oder mehrere Aktionen, jeweils mit Semikolon.

Beispiel:

chrono
Kopieren
Bearbeiten
loop every 10s if hour_between(9, 17) && mood == "tired" {
    log("Take a break");
    set mood = "relaxed";
}
Bedingungen
true / false

hour_between(start, end) — wahr, wenn aktuelle Stunde in [start, end)

date_is("YYYY-MM-DD") — wahr, wenn aktuelles Datum übereinstimmt

random_chance(p) — wahr mit Wahrscheinlichkeit p (0 ≤ p ≤ 1)

Bool-Operatoren:

&& → and

|| → or

! → not

Variablenvergleich z. B. mood == "relaxed"

Alle Ausdrücke landen als String in Python-eval(...) mit memory als Kontext.

Aktionen
log("<Text>"); — gibt <Text> (ohne Anführungszeichen) in der Konsole aus.

notify("<Text>"); — gibt <TEXT IN GROSSBUCHSTABEN> + „🔔“ aus.

wait(<TIME>); — pausiert den aktuellen Thread für <TIME> (z. B. 2s).

exec("<Python-Code>"); — führt echten Python-Code aus (im Kontext von memory).

chrono
Kopieren
Bearbeiten
exec("print('Status:', status)");
set <var> = <value>; — setzt Variable und schreibt memory.json neu.

Persistentes Memory (memory.json)
Beim Start versucht Chronoscript, eine Datei memory.json im Projektordner zu laden.

Ist sie vorhanden, wird der dort gespeicherte Zustand ins memory-Dict übernommen.

Fehlende Datei → leert memory.

Jedes Mal, wenn eine set-Aktion ausgeführt wird (Top-Level oder innerhalb eines Loops), speichert Chronoscript das aktualisierte memory-Dict in memory.json.

Beispiel-Inhalt:

json
Kopieren
Bearbeiten
{
  "status": "running",
  "mood": "productive"
}
Du kannst memory.json auch manuell editieren und das Skript dann neu starten, um mit vorgegebenen Variablen zu starten.

Beispielskripte
hello.chrono
chrono
Kopieren
Bearbeiten
loop every 10s if true {
    log("Hello, Chronoscript!");
}
memory.chrono
chrono
Kopieren
Bearbeiten
set mood = "tired";

loop every 5s if mood == "tired" {
    log("Take a break");
    set mood = "relaxed";
}

loop every 5s if mood == "relaxed" {
    notify("You seem better now!");
}
wait.chrono
chrono
Kopieren
Bearbeiten
loop every 5s if true {
    log("Start...");
    wait(3s);
    log("Waited 3 seconds!");
}
showcase.chrono
chrono
Kopieren
Bearbeiten
set status = "booting";
set mood = "neutral";

loop every 5s if true {
    log("Heartbeat: System running...");
    exec("print('Status:', status)");
    wait(2s);
    exec("print('>>> Python eval: status =', status)");
}

loop every 5s if hour_between(6, 9) && mood != "sleepy" {
    set mood = "sleepy";
    log("Good morning. Mood is sleepy.");
}

loop every 5s if hour_between(10, 17) && mood != "productive" {
    set mood = "productive";
    log("Work hours detected. Mood is productive.");
}

loop every 5s if hour_between(18, 22) && mood != "relaxed" {
    set mood = "relaxed";
    log("Evening. Mood is relaxed.");
}

loop every 5s if mood == "relaxed" {
    notify("Time to unwind ✨");
}

loop every 5s if mood == "productive" {
    log("Stay focused!");
    wait(1s);
    log("Keep up the good work.");
}

loop every 5s if random_chance(0.2) {
    notify("💡 Inspiration moment triggered!");
}
Troubleshooting
Parser-Fehler “Expected one of …”
Meist liegt das an einem ungültigen Zeichen ohne angepasste Grammatik.
– Kommentare mit // funktionieren nur, wenn COMMENT: /\/\/[^\n]*/ importiert und ignoriert wird.
– Stelle sicher, dass wait(2s) statt wait(2) steht.
– Kein + in Strings: Verwende exec("print('Status:', status)") statt notify("Status: " + status).

Variables nicht gefunden (name 'status' is not defined)
Tritt auf, wenn du in exec("…") verwendest, aber memory keinen Eintrag hat.
Stelle sicher, dass du vorher set status = "…", oder dass du beim Start von memory.json einen passenden Wert hast.

Speichern in memory.json funktioniert nicht
– Prüfe, ob die Datei schreibbar ist oder ob du sie versehentlich woanders hin verschoben hast.
– Bei mehrfachen set innerhalb kurzer Zeit kann es zu Race Conditions kommen. In Version 0.1 ist das nicht abgefedert; warte kurz ab oder starte neu.

Roadmap & weiterführende Ideen
Memory-Dump‐Befehl: Ein dump_memory(); als Aktion, um den aktuellen Zustand auch manuell auszugeben.

Mehr Datentypen: Listen und verschachtelte Dicts in memory.

HTTP/REST: call("GET", "https://api.example.com/data"); → JSON parsen und in Memory speichern.

User‐Input: input("Prompt> "); in Scripts für interaktive Abfragen.

TUI/GUI: Terminal-UI (z. B. mit textual) oder einfache Web­Dashboard zum Live-Monitoring der Loops.

Unit-Tests: Automatisierte Tests für Parser, Transformer, Interpreter (z. B. mit pytest).

Deploy als ausführbares Paket: via pyinstaller oder ein pip-Installable Package.