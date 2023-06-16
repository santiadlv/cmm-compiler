import sys

from .parser.cfg import CFG
from .parser.parser import Parser
from .scanner.scanner import Scanner


def scan_and_parse(filename: str) -> None:
    """Scan input and parse the tokens to check for syntactic errors."""
    cfg = CFG()
    cmm_scanner = Scanner(filename)
    lexical_output = cmm_scanner.scan()
    cmm_parser = Parser(cmm_scanner, cfg)
    
    parse_result = cmm_parser.parse()
    
    if parse_result:
        outfile = cmm_scanner.export_to_file(
            filename, *lexical_output
        )
        return outfile
    else:
        return None

if __name__ == "__main__":
    filenames = sys.argv[1:]
    try:
        for filename in filenames:
            outfile = scan_and_parse(filename)
            print(
                f"Scan output file for '{filename}' can be found at /output/{outfile}"
            )

    except FileNotFoundError:
        print(
            f"No such file or directory: '{filename}'. File could not be found in test"
            f" folder. Please try again."
        )
