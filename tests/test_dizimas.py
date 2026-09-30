"""
Testes Unitários para Detecção de Dízimas Periódicas Nativas.
"""

import unittest
from src.base_number import BaseNumber
from src.converter import convert


class TestDizimas(unittest.TestCase):

    def test_dizima_base4_to_base3(self):
        # (0.12)_4 = 1/4 + 2/16 = 3/8 = 0.375_10
        # Em base 3: 0.(10)_3
        num = BaseNumber.from_string("0.12", 4)
        res = convert(num, 3)
        self.assertTrue(res.is_periodic)
        self.assertEqual(res.period_start, 0)
        self.assertEqual(res.period_length, 2)
        self.assertEqual(res.result_number.to_string(), "0.(10)")

    def test_dizima_decimal_to_binary(self):
        # 0.1_10 em binário: 0.0(0011)_2
        num = BaseNumber.from_string("0.1", 10)
        res = convert(num, 2)
        self.assertTrue(res.is_periodic)
        self.assertEqual(res.period_start, 1)
        self.assertEqual(res.period_length, 4)
        self.assertEqual(res.result_number.to_string(), "0.0(0011)")

    def test_dizima_one_third_to_decimal(self):
        # 1/3 na base 3 é exatamente 0.1_3.
        # Convertido para decimal (base 10), gera a dízima 0.(3)_10.
        num = BaseNumber.from_string("0.1", 3)
        res = convert(num, 10)
        self.assertTrue(res.is_periodic)
        self.assertEqual(res.period_start, 0)
        self.assertEqual(res.period_length, 1)
        self.assertEqual(res.result_number.to_string(), "0.(3)")

    def test_dizima_one_seventh_to_decimal(self):
        # 1/7 na base 7 é exatamente 0.1_7.
        # Convertido para decimal (base 10), gera 0.(142857)_10.
        num = BaseNumber.from_string("0.1", 7)
        res = convert(num, 10)
        self.assertTrue(res.is_periodic)
        self.assertEqual(res.period_start, 0)
        self.assertEqual(res.period_length, 6)
        self.assertEqual(res.result_number.to_string(), "0.(142857)")


if __name__ == "__main__":
    unittest.main()
