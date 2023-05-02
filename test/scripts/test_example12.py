import pytest

from src.scanner.scanner import Scanner


class TestExample12:
    """Class to bundle tests for 'test12.cmm' file."""

    def scan(cls) -> tuple:
        """Create function to return results from scan."""
        filename = "test12.cmm"
        cmm_scanner = Scanner(filename)
        results = cmm_scanner.scan()
        return results
    
    def test_raise_invalid_exclamation_error(cls) -> None:
        """Test for invalid exclamation mark error."""
        with pytest.raises(Exception) as error:
            cls.scan()
        assert str(error.value) == "ERROR: Invalid character after '!' found at line 5"
