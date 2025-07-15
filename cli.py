import sys
from techlang.interpreter import run

def main():
    if len(sys.argv) != 2:
        print("Usage: python cli.py <filename.tl>")
        return

    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as f:
            code = f.read()
            result = run(code)
            print(result)
    except FileNotFoundError:
        print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
