from app.main import greet


def test_greet_includes_name():
    assert greet("Ada") == "Hello, Ada!"


def test_greet_empty_string():
    assert greet("") == "Hello, !"
