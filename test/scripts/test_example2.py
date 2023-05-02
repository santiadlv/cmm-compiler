import pytest

from src.scanner.scanner import Scanner


@pytest.fixture(scope="class")
def _scanner(request: pytest.FixtureRequest) -> None:
    """Fixture function to share results from scan to class."""
    filename = "test2.cmm"
    cmm_scanner = Scanner(filename)
    request.cls.results = cmm_scanner.scan()


@pytest.mark.usefixtures("_scanner")
class TestExample2:
    """Class to bundle tests for 'test2.cmm' file."""

    def test_output(cls) -> None:
        """Test for scanner output."""
        output = cls.results[0]
        expected_output = [
            (38, 1),
            1,
            (34, 1),
            26,
            (35, 1),
            27,
            20,
            3,
            (34, 2),
            20,
            2,
            (34, 3),
            20,
            2,
            (34, 4),
            26,
            (35, 1),
            27,
            20,
        ]
        assert output == expected_output

    def test_id_table(cls) -> None:
        """Test for scanner identifier symbol table."""
        id_symbol_table = cls.results[1]
        expected_id_symbol_table = {1: "x", 2: "s", 3: "f1", 4: "f2"}
        assert id_symbol_table == expected_id_symbol_table

    def test_int_table(cls) -> None:
        """Test for scanner integer symbol table."""
        int_symbol_table = cls.results[2]
        expected_int_symbol_table = {1: 10}
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
        expected_comment_symbol_table = {
            1: "/* Program that reads a 10 element array of\nintegers, and then multiply each element of\nthe array by a float, stores the result into an\narray of floats. Subsequently, the array of\nfloats is sorted and display it into standard\noutput.*/"
        }
        assert comment_symbol_table == expected_comment_symbol_table
