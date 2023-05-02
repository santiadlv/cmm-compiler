import pytest

from src.scanner.scanner import Scanner


class TestExample11:
    """Class to bundle tests for 'test11.cmm' file."""

    def scan(cls) -> tuple:
        """Create function to return results from scan."""
        filename = "test11.cmm"
        cmm_scanner = Scanner(filename)
        results = cmm_scanner.scan()
        return results
    
    def test_raise_invalid_symbol_error(cls) -> None:
        """Test for invalid symbol error."""
        with pytest.raises(Exception) as error:
            cls.scan()
        assert str(error.value) == "ERROR: Invalid complex symbol found at line 5"
