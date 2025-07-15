# techlang/parser.py

def parse(code: str) -> list:
    """
    Splits TechLang code into a list of commands.
    """
    return code.strip().split()
