class Tokens:
    """Custom class for the Scanner's Token helper."""
    
    def __init__(cls) -> None:
        """
        Define constructor method for the Tokens class.
        
        Properties:
            blank (dict): Set of blank characters
            digits (dict): Set of digits from 0 to 9
            letters (dict): Set of lower and uppercase letters from the alphabet
            special_characters (dict): Set of special characters
            complex_characters (dict): Set of a combination of special characters
            symbols (dict): Set of predefined symbols for symbol tables
            keywords (dict): Set of unique keywords of the language
            delimiters (dict): Union of blank, digit and special characters
            token_list (list): List of tokens, ordered as per the specification
            token_list_size (int): Size of the list of tokens
            token_ids (dict): Dictionary mapping tokens and their id's
        """
        cls.blank: dict = dict.fromkeys(["", " ", "\n", "\t", "\r"]).keys()
        cls.digits: dict = dict.fromkeys([*"0123456789"]).keys()
        cls.letters: dict = dict.fromkeys(
            [*"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ"]
        ).keys()
        cls.special_characters: dict = dict.fromkeys([*'+-*/<>=!;,".()[]{}']).keys()
        cls.complex_characters: dict = dict.fromkeys(["<=", ">=", "==", "!="]).keys()
        cls.symbols: dict = dict.fromkeys(
            ["ID", "INTEGER", "FLOAT", "STRING", "COMMENT"]
        ).keys()
        cls.keywords: dict = dict.fromkeys(
            [
                "int",
                "float",
                "string",
                "void",
                "if",
                "else",
                "for",
                "while",
                "read",
                "write",
                "return",
            ]
        ).keys()
        cls.delimiters: dict = cls.blank | cls.digits | cls.special_characters
        cls.token_list: list = cls.get_token_list()
        cls.token_list_size: int = len(cls.token_list)
        cls.token_ids: dict = dict(
            zip(cls.token_list, list(range(1, cls.token_list_size + 1)))
        )
        cls.tokens_by_id: dict = dict(
            zip(list(range(1, cls.token_list_size + 1)), cls.token_list)
        )

    def get_token_list(cls) -> list[list, list, list, list]:
        """
        Return the synthesis of all symbols to be tracked.

        Returns
            list[list, list, list, list]: List of lists from all possible symbols
        """
        return (
            list(cls.keywords)
            + list(cls.special_characters)
            + list(cls.complex_characters)
            + list(cls.symbols)
            + list("$")
        )

    def is_letter(cls, char: str) -> bool:
        """
        Check if character is a letter.

        Args:
            char (str): Character to check

        Returns:
            bool: Boolean stating whether char is letter or not
        """
        return char in cls.letters

    def is_digit(cls, char: str) -> bool:
        """
        Check if character is a digit.

        Args:
            char (str): Character to check

        Returns:
            bool: Boolean stating whether char is digit or not
        """
        return char in cls.digits

    def is_blank(cls, char: str) -> bool:
        """
        Check if character is blank.

        Args:
            char (str): Character to check

        Returns:
            bool: Boolean stating whether char is blank or not
        """
        return char in cls.blank

    def is_special_char(cls, char: str) -> bool:
        """
        Check if character is special char.

        Args:
            char (str): Character to check

        Returns:
            bool: Boolean stating whether char is special char or not
        """
        return char in cls.special_characters
    
    def is_keyword(cls, token: str) -> bool:
        """
        Check if character is keyword.

        Args:
            token (str): Character to check

        Returns:
            bool: Boolean stating whether char is keyword or not
        """
        return token.lower() in cls.keywords

    def identify_char(cls, char: str) -> str:
        """
        Identify which type of character is the supplied char.

        Args:
            char (str): Character to identify

        Returns:
            str: Description of whether it is a letter, digit, blank, special or invalid
        """
        if cls.is_letter(char):
            return "letter"
        elif cls.is_digit(char):
            return "digit"
        elif cls.is_blank(char):
            return "blank"
        elif cls.is_special_char(char):
            return char
        else:
            return "invalid"
