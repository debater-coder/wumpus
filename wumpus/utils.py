from typing import NoReturn


def assert_never(x: NoReturn) -> NoReturn:
    """A utility function used for exhaustive pattern matching."""
    assert False, "Unhandled type: {}".format(type(x).__name__)
