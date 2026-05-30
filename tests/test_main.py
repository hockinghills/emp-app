from app import __version__
from app.main import greet, main


def test_greet_includes_name():
    assert greet("Ada") == "Hello, Ada!"


def test_greet_empty_string():
    assert greet("") == "Hello, !"


def test_main_default_prints_hello(capsys):
    main([])
    assert capsys.readouterr().out.strip() == "Hello, world!"


def test_main_version_prints_version(capsys):
    main(["--version"])
    assert capsys.readouterr().out.strip() == __version__


def test_main_health_prints_ok(capsys):
    main(["--health"])
    assert capsys.readouterr().out.strip() == "ok"
