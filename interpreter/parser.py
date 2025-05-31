from lark import Lark

with open("interpreter/chrono_grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start")

def parse_chronoscript(text: str):
    return parser.parse(text)

if __name__ == "__main__":
    with open("examples/hello.chrono") as f:
        code = f.read()
    tree = parse_chronoscript(code)
    print(tree.pretty())
