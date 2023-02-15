from typing import Dict
from pathlib import Path

SRC_ROOT = [Path()]


def getDesc() -> Dict:
    """
    getDesc returns a dictionary describing the quality model.

    The keys of the dictionary are seen as characteristics of the model, and the
    values aggregation functions.
    """
    model = {"maintainability": maintainability, "duplication": duplication}
    return model


def maintainability():
    return 7 + duplication()


def duplication() -> int | float:
    return identical_blocks_of_code() + similar_blocks_of_code()


def cognitive_complexity():
    pass


def cyclomatic_complexity():
    pass


def argument_count():
    pass


def complex_logic():
    pass


def file_length():
    pass


def identical_blocks_of_code() -> int | float:
    return 2


def method_complexity():
    pass


def method_count():
    pass


def method_length():
    pass


def nested_control_flow():
    pass


def return_statements():
    pass


def similar_blocks_of_code() -> int | float:
    return 3
