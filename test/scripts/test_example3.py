import pytest

from src.scanner.scanner import Scanner


@pytest.fixture(scope="class")
def _scanner(request: pytest.FixtureRequest) -> None:
    """Fixture function to share results from scan to class."""
    filename = "test3.cmm"
    cmm_scanner = Scanner(filename)
    request.cls.results = cmm_scanner.scan()


@pytest.mark.usefixtures("_scanner")
class TestExample3:
    """Class to bundle tests for 'test3.cmm' file."""

    def test_output(cls) -> None:
        """Test for scanner output."""
        output = cls.results[0]
        expected_output = [
            1,
            (34, 1),
            24,
            2,
            (34, 2),
            26,
            27,
            21,
            1,
            (34, 3),
            21,
            1,
            (34, 4),
            25,
            28,
            1,
            (34, 5),
            20,
            2,
            (34, 6),
            20,
            1,
            (34, 7),
            20,
            (34, 7),
            18,
            (34, 3),
            20,
            (34, 6),
            18,
            (34, 2),
            26,
            (34, 3),
            27,
            20,
            (34, 5),
            18,
            (34, 3),
            12,
            (35, 1),
            20,
            8,
            24,
            (34, 5),
            16,
            (34, 4),
            25,
            28,
            5,
            24,
            (34, 2),
            26,
            (34, 5),
            27,
            16,
            (34, 8),
            25,
            28,
            (34, 6),
            18,
            (34, 2),
            26,
            (34, 5),
            27,
            20,
            (34, 7),
            18,
            (34, 5),
            20,
            29,
            (34, 5),
            18,
            (34, 5),
            12,
            (35, 1),
            20,
            29,
            11,
            (34, 7),
            20,
            29,
            (38, 1),
        ]
        assert output == expected_output

    def test_id_table(cls) -> None:
        """Test for scanner identifier symbol table."""
        id_symbol_table = cls.results[1]
        expected_id_symbol_table = {
            1: "miniloc",
            2: "a",
            3: "low",
            4: "high",
            5: "i",
            6: "y",
            7: "k",
            8: "x",
        }
        assert id_symbol_table == expected_id_symbol_table

    def test_int_table(cls) -> None:
        """Test for scanner integer symbol table."""
        int_symbol_table = cls.results[2]
        expected_int_symbol_table = {1: 1}
        assert int_symbol_table == expected_int_symbol_table

    def test_float_table(cls) -> None:
        """Test for scanner float symbol table."""
        float_symbol_table = cls.results[3]
        expected_float_symbol_table = {}
        assert float_symbol_table == expected_float_symbol_table

    def test_str_table(cls) -> None:
        """Test for scanner string symbol table."""
        str_symbol_table = cls.results[4]
        expected_str_symbol_table = {}
        assert str_symbol_table == expected_str_symbol_table

    def test_comment_table(cls) -> None:
        """Test for scanner comment symbol table."""
        comment_symbol_table = cls.results[5]
        expected_comment_symbol_table = {1: "/* END of miniloc() */"}
        assert comment_symbol_table == expected_comment_symbol_table
