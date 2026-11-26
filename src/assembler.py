"""Ассемблер УВМ: JSON -> промежуточное представление -> (этап 2) байты.

Этап 1: разбор JSON и вывод промежуточного представления в режиме тестирования.
"""

import argparse
import json
import sys
from typing import List

from .isa import (
    Instruction, OPCODES, OPERAND_MAP, validate
)


def parse_program(data: list) -> List[Instruction]:
    """Преобразует JSON-список в список Instruction."""
    program = []
    for idx, item in enumerate(data):
        if "op" not in item:
            raise ValueError(f"Элемент #{idx}: отсутствует поле 'op'")
        op = item["op"]
        if op not in OPERAND_MAP:
            raise ValueError(f"Элемент #{idx}: неизвестная команда {op!r}")
        fields = {}
        for operand, field_name in OPERAND_MAP[op].items():
            if operand not in item:
                raise ValueError(
                    f"Элемент #{idx} ({op}): отсутствует операнд {operand!r}"
                )
            fields[field_name] = item[operand]
        instr = Instruction(op=op, fields=fields)
        validate(instr)
        program.append(instr)
    return program


def print_test_view(program: List[Instruction]) -> None:
    """Выводит промежуточное представление в формате полей и значений."""
    print("=" * 60)
    print("Промежуточное представление программы (режим тестирования)")
    print("=" * 60)
    for i, instr in enumerate(program):
        a = OPCODES[instr.op]
        parts = [f"A={a}"]
        for fname in sorted(instr.fields):
            parts.append(f"{fname}={instr.fields[fname]}")
        print(f"[{i}] {instr.op}: " + ", ".join(parts))
    print("=" * 60)
    print(f"Всего команд: {len(program)}")

def encode(instr: Instruction) -> bytes:
    """Упаковывает Instruction в байты согласно спецификации УВМ."""
    word = OPCODES[instr.op] 
    for fname, value in instr.fields.items():
        shift, mask = FIELDS[instr.op][fname]
        word |= (value & mask) << shift
    return word.to_bytes(SIZES[instr.op], "little")


def encode_program(program: List[Instruction]) -> bytes:
    """Кодирует всю программу в единый поток байтов."""
    return b"".join(encode(i) for i in program)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Ассемблер учебной виртуальной машины (Вариант №1)"
    )
    parser.add_argument("source", help="Путь к JSON-файлу программы")
    parser.add_argument("output", help="Путь к бинарному файлу-результату")
    parser.add_argument(
        "--test", action="store_true",
        help="Режим тестирования: вывести промежуточное представление"
    )
    args = parser.parse_args(argv)

    with open(args.source, "r", encoding="utf-8") as f:
        data = json.load(f)

        binary = encode_program(program)
    with open(args.output, "wb") as f:
        f.write(binary)

    print(f"Ассемблировано команд: {len(program)}")

    if args.test:
        print_test_view(program)
        print("Байтовый код:")
        for i, instr in enumerate(program):
            raw = encode(instr)
            hex_str = ", ".join(f"0x{b:02X}" for b in raw)
            print(f"[{i}] {instr.op}: {hex_str}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
