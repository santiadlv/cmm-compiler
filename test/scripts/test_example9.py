import pytest

from src.scanner.scanner import Scanner


class TestExample9:
    """Class to bundle tests for 'test9.cmm' file."""

    def scan(cls) -> tuple:
        """Create function to return results from scan."""
        filename = "test9.cmm"
        cmm_scanner = Scanner(filename)
        results = cmm_scanner.scan()
        return results
    
    def test_raise_invalid_identifier_error(cls) -> None:
        """Test for invalid identifier error."""
        with pytest.raises(Exception) as error:
            cls.scan()
        assert str(error.value) == "ERROR: Invalid identifier found at line 1"
