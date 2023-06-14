import csv
from pathlib import Path


class CFG:
    """Class to represent a Context Free Grammar (CFG)."""

    def __init__(self) -> None:
        """Initialize constructor for CFG class."""
        self.grammar = self.read_grammar()
        self.grammar_nt = self.grammar[0]
        self.simple_nt = self.grammar[1]
        self.productions = self.read_productions()
        self.fp_sets = self.read_firstplus()
        self.num_productions = self.number_productions(self.productions)
        self.symbol_sets = self.compute_symbols(self.productions)
        self.symbols = self.symbol_sets[0]
        self.terminals = self.symbol_sets[1]
        self.non_terminals = self.symbol_sets[2]
        self.production_terminals = self.symbol_sets[3]
        self.table_set = self.create_parsing_table(
            self.terminals,
            self.non_terminals,
            self.num_productions,
            self.fp_sets,
            self.production_terminals,
            self.simple_nt,
        )
        self.table = self.table_set[0]
        self.ordered_t = self.table_set[1]


    def read_grammar(self) -> list:
        """
        Read the complete and simplified grammar from text files.

        Returns:
            list: Two lists containing the complete and
                  simplified grammar non terminal symbols.
        """
        grammar_nt = []
        path = Path.cwd().joinpath("data", "grammar.txt")

        with path.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()

            for line in lines:
                lhs = line.split("->")[0]
                grammar_nt.append(lhs)

        simple_nt = []
        path = Path.cwd().joinpath("data", "simple_grammar.txt")

        with path.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()

            for line in lines:
                lhs = line.split("->")[0]
                simple_nt.append(lhs)

        return grammar_nt, simple_nt


    def read_productions(self) -> list:
        """
        _summary_.

        Returns:
            list: _description_
        """
        productions = []
        path = Path.cwd().joinpath("data", "productions.txt")

        with path.open("r", encoding="utf-8") as f:
            productions = f.read().splitlines()

        return productions


    def read_firstplus(self) -> list:
        """
        _summary_.

        Returns:
            list: _description_

        """
        lines = []
        fp_sets = []
        path = Path.cwd().joinpath("data", "sets", "firstplus.txt")

        with path.open("r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        for fp_set in lines:
            rhs = fp_set.split(")={ ")[1][:-2]
            rhs_list = [terminal.strip() for terminal in rhs.split(" ")]
            fp_sets.append(rhs_list)

        return fp_sets


    def number_productions(self, productions: list) -> dict:
        """
        _summary_.

        Args:
            productions (list): _description_

        Returns:
            dict: _description_
        """
        num_productions = {}
        counter = 1

        for production in productions:
            num_productions[production] = counter
            counter += 1

        return num_productions


    def compute_symbols(self, productions: list) -> tuple:
        """
        _summary_.

        Args:
            productions (list): _description_

        Returns:
            tuple: _description_
        """
        symbols = set()
        terminals = set()
        non_terminals = set()
        production_terminals = []

        for production in productions:
            prod = production.split("->")
            lhs = prod[0]
            rhs = prod[1]
            non_terminals.add(lhs)
            prod_rhs_symbols = rhs.split(" ")
            production_terminals.append((lhs, prod_rhs_symbols))

            for symbol in prod_rhs_symbols:
                symbols.add(symbol)

        terminals = symbols - non_terminals - set("ε")
        return (
            symbols,
            terminals,
            non_terminals,
            production_terminals,
        )


    def create_parsing_table(
        self,
        terminals: set,
        non_terminals: set,
        num_productions: dict,
        fp_sets: list,
        production_terminals: list,
        simple_nt: list,
    ) -> tuple:
        """
        Create a parsing table for the given grammar for use in LL(1) parser.

        Args:
            terminals (set): Set of terminal symbols.
            non_terminals (set): Set of non terminal symbols.
            num_productions (dict): List of numbered productions.
            fp_sets (list): List of first plus sets.
            production_terminals (list): List of production terminals.
            simple_nt (list): List of simplified non terminal symbols.

        Returns:
            tuple: Both the parsing table and the ordered terminals.
        """
        table = {}
        ordered_t = sorted(terminals)
        ordered_t.append("$")

        ordering = {nt: i for i, nt in enumerate(simple_nt)}
        ordered_nt = sorted(list(non_terminals), key=lambda nt: ordering[nt])

        for nt in ordered_nt:
            table[nt] = {}

            for terminal in ordered_t:
                table[nt][terminal] = "ERROR"

        for prod, fp_set, pt in zip(num_productions, fp_sets, production_terminals):
            for terminal in fp_set:
                if terminal == "ε":
                    continue
                table[pt[0]][terminal] = num_productions[prod]

        return table, ordered_t


    def export_table(self) -> None:
        """Generate a CSV file of the parsing table."""
        path = Path.cwd().joinpath("data", "parsing_table.csv")
        field_names = ["non_terminal"] + self.ordered_t

        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=field_names)
            w.writeheader()

            for nt, st in zip(self.grammar_nt, self.simple_nt):
                row = {"non_terminal": nt} | self.table[st]
                w.writerow(row)

        print("Parsing table exported to data/parsing_table.csv")
