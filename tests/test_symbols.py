from slotmachine.symbols import string_compare
def test_exact_match():
    assert string_compare("R1", "R1")
def test_wild_match():
    assert string_compare("WW", "R1")
def test_non_match():
    assert not string_compare("R1", "E1")