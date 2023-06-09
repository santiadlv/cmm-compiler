from ..scanner.scanner import Scanner
from .cfg import CFG


class Parser:
    """Custom class for the Syntax Analyzer / Parser."""

    def __init__(self, scanner: Scanner, cfg: CFG) -> None:
        """Initialize constructor for Parser class."""
        self.scanner = scanner
        self.cfg = cfg

    def parse(self) -> bool:
        """Parse the tokens from the scanner to check for syntactic errors."""
        table = self.cfg.table
        token_identifier = self.scanner.token_helper.tokens_by_id
        input_tokens = [
            (self.scanner.token_helper.token_ids["$"],),
            *self.scanner.output[::-1],
        ]

        non_terminals = self.cfg.ordered_nt
        rhs_productions = self.cfg.rhs_productions

        stack = ["$"]
        stack.append(non_terminals[0])

        token_id = input_tokens.pop()
        next_token = input_tokens[-1]
        last_token = None

        while stack[-1] != "$":
            top = stack[-1]
            token = token_identifier[token_id[0]]

            # Check for a match between the top of the stack and the current token
            if top == token:
                print(f"Matched terminal: {token} on production {stack[-1]}")

                # Do small semantic analysis to enforce last function to be main
                if token == "void" and token_identifier[next_token[0]] == "ID":
                    idx = next_token[1]
                    name = self.scanner.id_symbol_table[idx]

                    if name == "main":
                        table["declaration_list"]["void"] = 3
                        stack = stack[:-7]

                # Pop the stack and get the next token
                stack.pop()
                last_token = token
                token_id = input_tokens.pop()

                if len(input_tokens) > 1:
                    next_token = input_tokens[-1]

            # If current token is terminal but is not the expected token, throw error
            elif top not in non_terminals:
                msg = f"Error: {top} is not a non-terminal symbol in production "
                msg += f"{stack[-1]}. Expected '{top}' but received '{token}' instead. "
                
                # Catch read statement error.
                if last_token == "read":
                    msg += "Read statement failed to parse."
                
                raise Exception(msg)
            # If current token is terminal not part of first plus set, throw error
            elif table[top][token] == "ERROR":
                filter_list = list(
                    filter(lambda x: x[1] != "ERROR", table[top].items())
                )
                expected = [x[0] for x in filter_list]
                msg = f"Error: Expected one of {expected} for production "
                msg += f"'{stack[-1]}' but received '{token}' instead."
                raise Exception(msg)
            else:
                # Get the RHS productions for the current token
                production_num = table[top][token]
                production_symbols = rhs_productions[production_num][::-1]

                # Pop the stack and push the RHS productions
                stack.pop()
                if "ε" not in production_symbols:
                    stack.extend(production_symbols)

        # Identify last token in input
        token = token_identifier[token_id[0]]

        # Verify last token and stack top are both "$"
        if stack[-1] == "$" and token == "$":
            print("Parsing successful.")
            return True
