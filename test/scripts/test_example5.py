import pytest

from src.scanner.scanner import Scanner


@pytest.fixture(scope="class")
def _scanner(request: pytest.FixtureRequest) -> None:
    """Fixture function to share results from scan to class."""
    filename = "test5.cmm"
    cmm_scanner = Scanner(filename)
    request.cls.results = cmm_scanner.scan()


@pytest.mark.usefixtures("_scanner")
class TestExample5:
    """Class to bundle tests for 'test5.cmm' file."""

    def test_output(cls) -> None:
        """Test for scanner output."""
        output = cls.results[0]
        expected_output = [
            4,
            (34, 1),
            24,
            4,
            25,
            28,
            1,
            (34, 2),
            20,
            (34, 3),
            18,
            (37, 1),
            20,
            10,
            24,
            (34, 3),
            25,
            20,
            9,
            24,
            (34, 4),
            25,
            20,
            8,
            24,
            (34, 2),
            16,
            (35, 1),
            25,
            28,
            (34, 3),
            18,
            (37, 2),
            20,
            10,
            24,
            (34, 3),
            25,
            20,
            9,
            (34, 5),
            26,
            (34, 2),
            27,
            20,
            (34, 6),
            26,
            (34, 2),
            27,
            18,
            (34, 5),
            26,
            (34, 2),
            27,
            14,
            (34, 4),
            20,
            (34, 2),
            18,
            (34, 2),
            12,
            (35, 2),
            20,
            29,
            11,
            20,
            29,
            (38, 1),
        ]
        assert output == expected_output

    def test_id_table(cls) -> None:
        """Test for scanner identifier symbol table."""
        id_symbol_table = cls.results[1]
        expected_id_symbol_table = {
            1: "readArray",
            2: "i",
            3: "s",
            4: "f1",
            5: "x",
            6: "f2",
        }
        assert id_symbol_table == expected_id_symbol_table

    def test_int_table(cls) -> None:
        """Test for scanner integer symbol table."""
        int_symbol_table = cls.results[2]
        expected_int_symbol_table = {1: 10, 2: 1}
        assert int_symbol_table == expected_int_symbol_table

    def test_float_table(cls) -> None:
        """Test for scanner float symbol table."""
        float_symbol_table = cls.results[3]
        expected_float_symbol_table = {}
        assert float_symbol_table == expected_float_symbol_table

    def test_str_table(cls) -> None:
        """Test for scanner string symbol table."""
        str_symbol_table = cls.results[4]
        expected_str_symbol_table = {
            1: '"Enter a float number: "',
            2: '"Enter an integer number: "',
        }
        assert str_symbol_table == expected_str_symbol_table

    def test_comment_table(cls) -> None:
        """Test for scanner comment symbol table."""
        comment_symbol_table = cls.results[5]
        expected_comment_symbol_table = {1: "/* END of readArray() */"}
        assert comment_symbol_table == expected_comment_symbol_table
