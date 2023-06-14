import sys

from .parser.cfg import CFG
from .scanner.scanner import Scanner

if __name__ == "__main__":
    filenames = sys.argv[1:]
    try:
        for filename in filenames:
            cmm_scanner = Scanner(filename)
            output, ids, ints, floats, strings, comments = cmm_scanner.scan()
            output_file = cmm_scanner.export_to_file(
                filename, output, ids, ints, floats, strings, comments
            )
            print(f"Output file for '{filename}' can be found at /output/{output_file}")
            
            cfg = CFG()
            print(cfg.table)
    except FileNotFoundError:
        print(
            f"No such file or directory: '{filename}'. File could not be found in test"
            f" folder. Please try again."
        )
