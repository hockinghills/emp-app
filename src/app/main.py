from app import __version__


def greet(name: str) -> str:
    return f"Hello, {name}!"


def main(argv: list[str] | None = None) -> None:
    import sys

    args = sys.argv[1:] if argv is None else argv
    if args and args[0] in ("--version", "-V"):
        print(__version__)
        return
    if args and args[0] in ("--health", "healthz"):
        print("ok")
        return
    print(greet("world"))


if __name__ == "__main__":
    main()
