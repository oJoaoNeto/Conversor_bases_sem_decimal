"""
Testes Unitários para Conversão Direta entre Bases Arbitrárias.
"""

import unittest
from src.base_number import BaseNumber
from src.converter import convert


class TestConverter(unittest.TestCase):

    def test_convert_integer_binary_to_hex(self):
        # 1101111010101101_2 == DEAD_16
        num = BaseNumber.from_string("1101111010101101", 2)
        res = convert(num, 16)
        self.assertEqual(res.result_number.to_string(), "DEAD")

    def test_convert_integer_hex_to_binary(self):
        # DEAD_16 == 1101111010101101_2
        num = BaseNumber.from_string("DEAD", 16)
        res = convert(num, 2)
        self.assertEqual(res.result_number.to_string(), "1101111010101101")

    def test_convert_base7_to_base13(self):
        # Mencionada explicitamente no PDF do professor!
        # (25)_7 = 2*7 + 5 = 19_10.
        # Em base 13: 19 = 1*13 + 6 = (16)_13.
        num = BaseNumber.from_string("25", 7)
        res = convert(num, 13)
        self.assertEqual(res.result_number.to_string(), "16")

        # (66)_7 = 6*7 + 6 = 48_10.
        # Em base 13: 48 = 3*13 + 9 = (39)_13.
        num2 = BaseNumber.from_string("66", 7)
        res2 = convert(num2, 13)
        self.assertEqual(res2.result_number.to_string(), "39")

    def test_convert_real_finite(self):
        # 13.625_10 para Base 2 -> 1101.101_2
        num = BaseNumber.from_string("13.625", 10)
        res = convert(num, 2)
        self.assertEqual(res.result_number.to_string(), "1101.101")
        self.assertFalse(res.is_periodic)

    def test_convert_real_octal_to_hex(self):
        # 15.5_8 = 13 + 5/8 = 13.625_10
        # Em hex: 13.625 = D + 10/16 = D.A_16
        num = BaseNumber.from_string("15.5", 8)
        res = convert(num, 16)
        self.assertEqual(res.result_number.to_string(), "D.A")

    def test_convert_negative_real(self):
        # -13.625_10 para Base 2 -> -1101.101_2
        num = BaseNumber.from_string("-13.625", 10)
        res = convert(num, 2)
        self.assertEqual(res.result_number.to_string(), "-1101.101")

    def test_convert_zero(self):
        num = BaseNumber.from_string("0.0", 5)
        res = convert(num, 9)
        self.assertEqual(res.result_number.to_string(), "0")


if __name__ == "__main__":
    unittest.main()
