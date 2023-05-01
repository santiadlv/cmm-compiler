import csv
from pathlib import Path


class TransitionTable:
    """Custom class for the Scanner's transition table helper."""
    
    def __init__(cls) -> None:
        """
        Define constructor method for the TransitionTable class.
        
        Properties:
            filename (str): file from where to read transitions in CSV format
            path (Path): Path object to handle paths and file opening
            accepted (list): List of final, accepting states
            error (list): List of final, error states
            consuming (list): List of states that consume characters when read
            table (list): Transition table data structure
            keys (list): Keys for recognizing transition inputs
            id_state (int): State for successful identifiers
            int_state (int): State for successful integer constants
            float_state (int): State for successful floating point constants
            str_state (int): State for successful strings
            comment_state (int): State for successful comments
            active_states (list): List of states that have yet to finish
            incomplete_commment (list): List of states where comments are not closed yet
            incomplete_string (int): State where strings are not closed yet
        """
        cls.filename: str = "transitions.csv"
        cls.path: Path = Path.cwd().joinpath("data", cls.filename)
        cls.accepted: list = list(range(13, 36 + 1))
        cls.error: list = [37, 38, 39, 40, 41]
        cls.consuming: list = [13, 14, 15, 16, 19, 21, 23]
        cls.table: list = cls.generate_table()
        cls.keys: list = []
        cls.id_state: int = 13
        cls.int_state: int = 14
        cls.float_state: int = 15
        cls.str_state: int = 18
        cls.comment_state: int = 17
        cls.active_states: list = [5, 7, 8]
        cls.incomplete_comment: list = [7, 8]
        cls.incomplete_string: int = 5

    def generate_table(cls) -> list:
        """
        Iterate through the CSV file and append transitions for each input character.

        Returns
            list: List specifying the transition table of the scanner
        """
        table = []
        with cls.path.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=",")
            for i, states in enumerate(reader):
                if i == 0:
                    cls.keys = states
                    continue
                transition = {}
                for j, value in enumerate(states):
                    transition[cls.keys[j]] = value
                table.append(transition)
        return table

    def is_acceptor_state(cls, state: int) -> bool:
        """
        Check if state is acceptor.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is acceptor or not
        """
        return state in cls.accepted

    def is_error_state(cls, state: int) -> bool:
        """
        Check if state is error.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is error or not
        """
        return state in cls.error
    
    def is_consuming_state(cls, state: int) -> bool:
        """
        Check if state is consuming.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is consuming or not
        """
        return state in cls.consuming
    
    def is_active_state(cls, state: int) -> bool:
        """
        Check if state is active.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is active or not
        """
        return state in cls.active_states
    
    def is_incomplete_comment(cls, state: int) -> bool:
        """
        Check if state is part of incomplete comments.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is an incomplete comment or not
        """
        return state in cls.incomplete_comment
    
    def is_incomplete_string(cls, state: int) -> bool:
        """
        Check if state is part of incomplete strings.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is an incomplete string or not
        """
        return state == cls.incomplete_string
    
    def is_identifier(cls, state: int) -> bool:
        """
        Check if state is an identifier.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is an identifier or not
        """
        return state == cls.id_state
    
    def is_integer(cls, state: int) -> bool:
        """
        Check if state is an integer constant.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is an integer or not
        """
        return state == cls.int_state
    
    def is_float(cls, state: int) -> bool:
        """
        Check if state is a floating point constant.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is a float or not
        """
        return state == cls.float_state
    
    def is_string(cls, state: int) -> bool:
        """
        Check if state is a string.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is a string or not
        """
        return state == cls.str_state
    
    def is_comment(cls, state: int) -> bool:
        """
        Check if state is a comment.

        Args:
            state (int): State to be checked

        Returns:
            bool: Boolean stating whether state is a comment or not
        """
        return state == cls.comment_state
