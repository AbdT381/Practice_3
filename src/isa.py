"""Описание набора команд УВМ (Вариант №1)."""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class Instruction:
    """Промежуточное представление одной команды."""
    op: str
    fields: Dict[str, int] = field(default_factory=dict)

    def __repr__(self) -> str:
        inner = ", ".join(f"{k}={v}" for k, v in self.fields.items())
        return f"Instruction(op={self.op!r}, {inner})"


""" Код операции (поле A)"""
OPCODES = {
    "load_const": 92,
    "read_mem": 194,
    "write_mem": 207,
    "mul": 30,
}

"""Размер команды в байтах"""
SIZES = {
    "load_const": 5,
    "read_mem": 6,
    "write_mem": 3,
    "mul": 4,
}

# Спецификация битовых полей: имя -> (сдвиг, маска)
FIELDS = {
    "load_const": {"B": (8, 0x7F), "C": (15, 0x1FFFFF)},
    "read_mem":   {"B": (8, 0x7F), "C": (15, 0x7FFFFFF)},
    "write_mem":  {"B": (8, 0x7F), "C": (15, 0x7F)},
    "mul":        {"B": (8, 0x7F), "C": (15, 0x7F), "D": (22, 0x7F)},
}

"""Отображение операндов JSON -> поля B/C/D"""
OPERAND_MAP = {
    "load_const": {"addr": "B", "value": "C"},
    "read_mem":   {"dst": "B", "src": "C"},
    "write_mem":  {"src": "B", "addr_reg": "C"},
    "mul":        {"a": "D", "b": "B", "dst": "C"},
}


def validate(instr: Instruction) -> None:
    """Проверяет корректность команды и диапазоны значений."""
    if instr.op not in OPCODES:
        raise ValueError(f"Неизвестная команда: {instr.op}")
    expected = set(OPERAND_MAP[instr.op].values())
    if set(instr.fields.keys()) != expected:
        raise ValueError(
            f"{instr.op}: ожидались поля {expected}, получены {set(instr.fields)}"
        )
    for fname, value in instr.fields.items():
        _, mask = FIELDS[instr.op][fname]
        if not (0 <= value <= mask):
            raise ValueError(
                f"{instr.op}.{fname}={value} вне диапазона 0..{mask}"
            )
