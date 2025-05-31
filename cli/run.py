import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interpreter.parser import parser
from interpreter.transformer import ChronoTransformer
from interpreter.interpreter import run_script

def main():
    parser_arg = argparse.ArgumentParser(description="Run a Chronoscript file.")
    parser_arg.add_argument("file", type=str, help="Path to the .chrono file")
    args = parser_arg.parse_args()

    if not os.path.isfile(args.file):
        print(f"[error] File not found: {args.file}")
        sys.exit(1)

    with open(args.file, "r") as f:
        code = f.read()

    try:
        tree = parser.parse(code)
        data = ChronoTransformer().transform(tree)
        run_script(data)
    except Exception as e:
        print(f"[error] Failed to execute script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
