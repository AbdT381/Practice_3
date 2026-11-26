"""Пакет ассемблера и интерпретатора УВМ (Вариант №1).

Реэкспортирует ключевые сущности для удобства:
    from src import Instruction, OPCODES, parse_program
"""

from .isa import (
    Instruction,
    OPCODES,
    SIZES,
    FIELDS,
    OPERAND_MAP,
    validate,
)
from .assembler import parse_program, print_test_view

__all__ = [
    "Instruction",
    "OPCODES",
    "SIZES",
    "FIELDS",
    "OPERAND_MAP",
    "validate",
    "parse_program",
    "print_test_view",
]

__version__ = "0.1.0"
