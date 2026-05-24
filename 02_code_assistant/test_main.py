from main import is_palindrome


def test_palindrome_simple():
    assert is_palindrome("madam") == True


def test_not_palindrome():
    assert is_palindrome("hello") == False


def test_case_insensitive():
    assert is_palindrome("RaceCar") == True


def test_single_character():
    assert is_palindrome("a") == True


def test_empty_string():
    assert is_palindrome("") == True
