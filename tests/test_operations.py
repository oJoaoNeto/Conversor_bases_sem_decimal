"""
Testes Unitários para Operações Elementares (Adição e Subtração).
"""

import unittest
from src.base_number import BaseNumber
from src.operations import add, subtract, scalar_multiply


class TestOperations(unittest.TestCase):

    def test_addition_simple(self):
        # Base 10: 12.3 + 4.5 = 16.8
        a = BaseNumber.from_string("12.3", 10)
        b = BaseNumber.from_string("4.5", 10)
        res, trace = add(a, b)
        self.assertEqual(res.to_string(), "16.8")

    def test_addition_carry_cascade_binary(self):
        # Base 2: 111 + 1 = 1000
        a = BaseNumber.from_string("111", 2)
        b = BaseNumber.from_string("1", 2)
        res, _ = add(a, b)
        self.assertEqual(res.to_string(), "1000")

    def test_addition_carry_hex(self):
        # Base 16: FF.8 + 0.8 = 100
        a = BaseNumber.from_string("FF.8", 16)
        b = BaseNumber.from_string("0.8", 16)
        res, _ = add(a, b)
        self.assertEqual(res.to_string(), "100")

    def test_addition_fractional_alignment(self):
        # Base 8: 3.14 + 12.5 = 15.64
        a = BaseNumber.from_string("3.14", 8)
        b = BaseNumber.from_string("12.5", 8)
        res, _ = add(a, b)
        self.assertEqual(res.to_string(), "15.64")

    def test_addition_signs(self):
        # Sinais opostos com |A| > |B|: 15 + (-7) = 8
        a = BaseNumber.from_string("15", 10)
        b = BaseNumber.from_string("-7", 10)
        res, _ = add(a, b)
        self.assertEqual(res.to_string(), "8")

        # Sinais opostos com |A| < |B|: 7 + (-15) = -8
        c = BaseNumber.from_string("7", 10)
        d = BaseNumber.from_string("-15", 10)
        res2, _ = add(c, d)
        self.assertEqual(res2.to_string(), "-8")

        # Ambos negativos: (-5) + (-6) = -11
        e = BaseNumber.from_string("-5", 10)
        f = BaseNumber.from_string("-6", 10)
        res3, _ = add(e, f)
        self.assertEqual(res3.to_string(), "-11")

        # Soma resultando em zero: 10 + (-10) = 0
        g = BaseNumber.from_string("10", 10)
        h = BaseNumber.from_string("-10", 10)
        res4, _ = add(g, h)
        self.assertEqual(res4.to_string(), "0")

    def test_subtraction_simple(self):
        # Base 10: 58.7 - 23.4 = 35.3
        a = BaseNumber.from_string("58.7", 10)
        b = BaseNumber.from_string("23.4", 10)
        res, trace = subtract(a, b)
        self.assertEqual(res.to_string(), "35.3")

    def test_subtraction_borrow_cascade_binary(self):
        # Base 2: 1000 - 1 = 111
        a = BaseNumber.from_string("1000", 2)
        b = BaseNumber.from_string("1", 2)
        res, trace = subtract(a, b)
        self.assertEqual(res.to_string(), "111")
        # Confirma que houve borrow
        self.assertTrue(any(b > 0 for b in trace.borrows_int))

    def test_subtraction_borrow_hex(self):
        # Base 16: 100 - 1 = FF
        a = BaseNumber.from_string("100", 16)
        b = BaseNumber.from_string("1", 16)
        res, _ = subtract(a, b)
        self.assertEqual(res.to_string(), "FF")

    def test_subtraction_borrow_fractional(self):
        # Base 2: 1.0 - 0.1 = 0.1
        a = BaseNumber.from_string("1.0", 2)
        b = BaseNumber.from_string("0.1", 2)
        res, _ = subtract(a, b)
        self.assertEqual(res.to_string(), "0.1")

    def test_subtraction_negative_result(self):
        # Base 16: 10 - 25 = -15 (em hex: 10_16 = 16, 25_16 = 37, 16 - 37 = -21 = -15_16)
        a = BaseNumber.from_string("10", 16)
        b = BaseNumber.from_string("25", 16)
        res, trace = subtract(a, b)
        self.assertEqual(res.to_string(), "-15")
        self.assertTrue(trace.swapped_operands)

    def test_scalar_multiply(self):
        # Base 3: (11)_3 * 2 = (22)_3
        a = BaseNumber.from_string("11", 3)
        res = scalar_multiply(a, 2)
        self.assertEqual(res.to_string(), "22")

        # Base 16: (A)_16 * 16 = (A0)_16
        b = BaseNumber.from_string("A", 16)
        res2 = scalar_multiply(b, 16)
        self.assertEqual(res2.to_string(), "A0")


if __name__ == "__main__":
    unittest.main()
