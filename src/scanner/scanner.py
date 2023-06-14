import sys
from pathlib import Path

from .tokens import Tokens
from .transition_table import TransitionTable


class Scanner:
    """Custom class for the Lexical Analyzer / Scanner."""

    def __init__(cls, filename: str) -> None:
        """
        Define constructor method for the Scanner class.

        Args:
            filename (str): Filename of the file to be analyzed

        Properties:
            output (list): List where the scanner output will be saved
            token_helper (Tokens): Local imported class regarding Tokens
            automaton (TransitionTable): Local imported class regarding Transitions
            filename (str): The filename of the file that is going to be analyzed
            path (Path): OS library to simplify path and file handling
            id_symbol_table (dict): Symbol table to save identifiers
            int_symbol_table (dict): Symbol table to save integer numbers
            float_symbol_table (dict): Symbol table to save floating point numbers
            string_symbol_table (dict): Symbol table to save strings
            comment_symbol_table (dict): Symbol table to save comments
            error_messages (dict): Dictionary with error messages and their states
        """
        cls.output: list = []
        cls.token_helper: Tokens = Tokens()
        cls.automaton: TransitionTable = TransitionTable()
        cls.filename: str = filename
        cls.path: Path = Path.cwd().joinpath("test", "examples", cls.filename)
        cls.id_symbol_table: dict = {}
        cls.int_symbol_table: dict = {}
        cls.float_symbol_table: dict = {}
        cls.string_symbol_table: dict = {}
        cls.comment_symbol_table: dict = {}
        cls.error_messages: dict = dict(
            zip(
                cls.automaton.error,
                [
                    "Invalid identifier found",
                    "Invalid number found",
                    "Invalid character after '!' found",
                    "Invalid character found",
                    "Invalid complex symbol found",
                ],
            )
        )

    def existing_symbol(cls, token: str, symbol_table: dict) -> bool:
        """
        Check if a symbol was already saved in a symbol table.

        Args:
            token (str): The token to be checked
            symbol_table (dict): The symbol table where the check will happen

        Returns:
            bool: A boolean value specifying whether the symbol was previously saved
        """
        return True if token in symbol_table.values() else False

    def add_token_to_symbol_table(cls, token: str, symbol_table: dict) -> None:
        """
        Add a token to the specified symbol table if it doesn't exist already.

        Args:
            token (str): The token to be added
            symbol_table (dict): The symbol table where the token will be added
        """
        if not cls.existing_symbol(token, symbol_table):
            entry = len(symbol_table) + 1
            symbol_table[entry] = token

    def add_symbol_to_output(cls, token: str, symbol_table: dict, t_id: str) -> None:
        """
        Append a built symbol to the output list of the Scanner.

        Args:
            token (str): Token to be added to the output
            symbol_table (dict): Symbol table corresponding to the token of the symbol
            t_id (str): Identifier of the token to be retrieved from the Token ID table
        """
        idx = next((k for k in symbol_table if symbol_table[k] == token), None)
        cls.output.append((cls.token_helper.token_ids[t_id], idx))

    def scan(cls) -> tuple[list, dict, dict, dict, dict, dict]:
        """
        Scan method responsible for retrieving, identifying and saving tokens from the
        source file specified.

        Raises
            Exception: Raised if a comment was not closed correctly
            Exception: Raised if a string was not closed correctly
            Exception: Raised depending on the error state, with its own error message
            Exception: Raised in case an unknown error was thrown

        Returns
            tuple[list, dict, dict, dict, dict, dict]: Tuple with output and all symbol
                                                       tables

        """
        # Initialize local scoped variables for scanner execution
        dfa = cls.automaton
        tkn = cls.token_helper
        char = ""
        lookbehind = ""
        token = ""
        state = 0
        line = 1
        str_offset = 0
        cmt_offset = 0

        with cls.path.open(encoding="utf-8") as file:
            while True:
                # Run while state is not acceptor, error, or there is a lookbehind char
                while (
                    not dfa.is_acceptor_state(state) and not dfa.is_error_state(state)
                ) or lookbehind != "":
                    if lookbehind == "":
                        char = file.read(1)
                    else:
                        char = lookbehind
                        lookbehind = ""

                    # If last char was read already, break the loop
                    if not char and token == "":
                        break

                    # If newline char is read, increase line count and set offsets
                    if char == "\n":
                        line += 1
                        if dfa.is_active_state(state):
                            if dfa.is_incomplete_comment(state):
                                cmt_offset += 1
                            else:
                                str_offset += 1

                    # Identify character type and get state from transition table
                    char_type = tkn.identify_char(char)
                    state = int(dfa.table[state][char_type])

                    if not tkn.is_blank(char) or dfa.is_active_state(state):
                        token += char
                        
                    # If last char and state is in incomplete comment, break the loop
                    if not char and (
                        dfa.is_incomplete_comment(state)
                        or dfa.is_incomplete_string(state)
                    ):
                        break

                # Break loop if tokens are depleted and state is not active
                if not char and token == "" and not dfa.is_active_state(state):
                    break

                # Check if state is a final accepting state
                if dfa.is_acceptor_state(state):
                    # If state is consuming and char is not blank, set lookbehind
                    if dfa.is_consuming_state(state) and not tkn.is_blank(char):
                        lookbehind = token[-1]
                        token = token[:-1]

                    if dfa.is_identifier(state):
                        # If token is a keyword
                        if tkn.is_keyword(token.lower()):
                            cls.output.append((tkn.token_ids[token.lower()]))
                        else:
                            # If token is not a keyword
                            cls.add_token_to_symbol_table(token, cls.id_symbol_table)
                            cls.add_symbol_to_output(
                                token, cls.id_symbol_table, "IDENTIFIER"
                            )
                    elif dfa.is_integer(state):
                        # Cast token in case it is an integer constant
                        token = int(token)
                        cls.add_token_to_symbol_table(token, cls.int_symbol_table)
                        cls.add_symbol_to_output(
                            token, cls.int_symbol_table, "INT_CONST"
                        )
                    elif dfa.is_float(state):
                        # Cast token in case it is a floating point constant
                        token = float(token)
                        cls.add_token_to_symbol_table(token, cls.float_symbol_table)
                        cls.add_symbol_to_output(
                            token, cls.float_symbol_table, "FLOAT_CONST"
                        )
                    elif dfa.is_string(state):
                        # If token is a string, persist and reset offset
                        str_offset = 0
                        cls.add_token_to_symbol_table(token, cls.string_symbol_table)
                        cls.add_symbol_to_output(
                            token, cls.string_symbol_table, "STRING"
                        )
                    elif dfa.is_comment(state):
                        # If token is a comment, persist and reset offset
                        cmt_offset = 0
                        cls.add_token_to_symbol_table(token, cls.comment_symbol_table)
                        # cls.add_symbol_to_output(
                        #     token, cls.comment_symbol_table, "COMMENT"
                        # )
                    else:
                        # Search the token's ID and persist to output
                        cls.output.append((tkn.token_ids[token]))

                    # Reset both state and token variables for next character
                    state = 0
                    token = ""

                elif dfa.is_incomplete_comment(state):
                    raise Exception(
                        f"ERROR: Incorrectly closed comment in line {line - cmt_offset}"
                    )
                elif dfa.is_incomplete_string(state):
                    raise Exception(
                        f"ERROR: Incorrectly closed string in line {line - str_offset}"
                    )
                elif dfa.is_error_state(state):
                    raise Exception(
                        f"ERROR: {cls.error_messages[state]} at line {line}"
                    )
                else:
                    raise Exception("Unkwown error occurred")

        return (
            cls.output,
            cls.id_symbol_table,
            cls.int_symbol_table,
            cls.float_symbol_table,
            cls.string_symbol_table,
            cls.comment_symbol_table,
        )

    def export(
        cls,
        filename: str,
        output: list,
        ids: dict,
        ints: dict,
        floats: dict,
        strings: dict,
        comments: dict,
    ) -> None:
        """
        Print output and symbol tables to stdout.

        Args:
            filename (str): Name of the file to be analyzed
            output (list): Output list with all identified tokens
            ids (dict): Symbol table with identifiers
            ints (dict): Symbol table with integer constants
            floats (dict): Symbol table with floating gpoint constants
            strings (dict): Symbol table with strings
            comments (dict): Symbol table with comments
        """
        print("\n" + "=" * 30)
        print(f"Results for file: '{filename}'")
        print("=" * 30 + "\n")
        print(f"TOKEN_IDS: {cls.token_helper.token_ids}\n")
        print(f"OUTPUT: {output}\n")
        print(f"IDS (34): {ids}\n")
        print(f"INTS (35): {ints}\n")
        print(f"FLOATS (36): {floats}\n")
        print(f"STRINGS (37): {strings}\n")
        print(f"COMMENTS (38): {comments}\n")

    def export_to_file(
        cls,
        filename: str,
        output: list,
        ids: dict,
        ints: dict,
        floats: dict,
        strings: dict,
        comments: dict,
    ) -> None:
        """
        Print output and symbol tables to a file.

        Args:
            filename (str): Name of the file to be analyzed
            output (list): Output list with all identified tokens
            ids (dict): Symbol table with identifiers
            ints (dict): Symbol table with integer constants
            floats (dict): Symbol table with floating gpoint constants
            strings (dict): Symbol table with strings
            comments (dict): Symbol table with comments
        """
        prev_stdout = sys.stdout

        output_filename = f"{filename}_output.txt"
        output_file = Path.cwd().joinpath("output", output_filename)

        with open(output_file, "w", encoding="utf-8") as file:
            sys.stdout = file

            print("=" * 30)
            print(f"Results for file: '{filename}'")
            print("=" * 30 + "\n")
            print(f"TOKEN_IDS: {cls.token_helper.token_ids}\n")
            print(f"OUTPUT: {output}\n")
            print(f"IDS (34): {ids}\n")
            print(f"INTS (35): {ints}\n")
            print(f"FLOATS (36): {floats}\n")
            print(f"STRINGS (37): {strings}\n")
            print(f"COMMENTS (38): {comments}\n")

            sys.stdout = prev_stdout

        return output_filename
