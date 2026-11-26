"""Тесты ассемблера УВМ (Этап 1)."""

import unittest

from src.assembler import parse_program
from src.isa import OPCODES


SPEC = [
    {"op": "load_const", "addr": 96,  "value": 337},
    {"op": "read_mem",   "dst": 127,  "src": 681},
    {"op": "write_mem",  "src": 67,   "addr_reg": 1},
    {"op": "mul",        "dst": 36,   "a": 9,   "b": 66},
]


class TestAssembler(unittest.TestCase):

    def test_parse_and_fields(self):
        prog = parse_program(SPEC)
        self.assertEqual(len(prog), 4)

        self.assertEqual(prog[0].op, "load_const")
        self.assertEqual(prog[0].fields, {"B": 96, "C": 337})

        self.assertEqual(prog[1].op, "read_mem")
        self.assertEqual(prog[1].fields, {"B": 127, "C": 681})

        self.assertEqual(prog[2].op, "write_mem")
        self.assertEqual(prog[2].fields, {"B": 67, "C": 1})

        self.assertEqual(prog[3].op, "mul")
        self.assertEqual(prog[3].fields, {"D": 9, "B": 66, "C": 36})

    def test_opcodes(self):
        self.assertEqual(OPCODES["load_const"], 92)
        self.assertEqual(OPCODES["read_mem"], 194)
        self.assertEqual(OPCODES["write_mem"], 207)
        self.assertEqual(OPCODES["mul"], 30)

    def test_missing_operand(self):
        with self.assertRaises(ValueError):
            parse_program([{"op": "load_const", "addr": 1}])

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            parse_program([{"op": "write_mem", "src": 1, "addr_reg": 200}])

    def test_unknown_op(self):
        with self.assertRaises(ValueError):
            parse_program([{"op": "nop"}])


if __name__ == "__main__":
    unittest.main()
