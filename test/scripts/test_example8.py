import pytest

from src.scanner.scanner import Scanner


class TestExample8:
    """Class to bundle tests for 'test8.cmm' file."""

    def scan(cls) -> tuple:
        """Create function to return results from scan."""
        filename = "test8.cmm"
        cmm_scanner = Scanner(filename)
        results = cmm_scanner.scan()
        return results
    
    def test_raise_invalid_character_error(cls) -> None:
        """Test for invalid character error."""
        with pytest.raises(Exception) as error:
            cls.scan()     
        assert str(error.value) == "ERROR: Invalid character found at line 1"
