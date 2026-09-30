"""
Programa Principal / Interface CLI Interativa
ECT-3401: Computação Numérica - Unidade I
Conversão de Bases e Operações Elementares em Ponto Flutuante Sem Coerção Decimal.
"""

import sys
from typing import Optional

# Garante suporte a UTF-8 em terminais Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src.base_number import BaseNumber
from src.operations import add, subtract
from src.converter import convert
from src.display import (
    format_addition_conta_armada,
    format_subtraction_conta_armada,
    format_conversion_report,
)


def banner():
    print(r"""
========================================================================
   ECT-3401: COMPUTAÇÃO NUMÉRICA - PROJETO UNIDADE I (UFRN)
   Conversão Direta de Bases & Operações Elementares Sem Pivô Decimal
========================================================================
""")


def menu_operacoes():
    print("\n--- MENU: OPERAÇÕES ELEMENTARES ---")
    try:
        base = int(input("Informe a base numérica dos operandos (2 a 36): ").strip())
        num1_str = input(f"Primeiro operando na base {base} (ex: 1A.4, -0.5, etc): ").strip()
        num2_str = input(f"Segundo operando na base {base}: ").strip()

        a = BaseNumber.from_string(num1_str, base)
        b = BaseNumber.from_string(num2_str, base)

        print("\nEscolha a operação:")
        print("  1. Adição (A + B)")
        print("  2. Subtração (A - B)")
        op_choice = input("Opção (1 ou 2): ").strip()

        if op_choice == "1":
            res, trace = add(a, b)
            print("\n" + format_addition_conta_armada(trace))
            print(f"\nResultado Final: {res.to_string()} (Base {base})")
        elif op_choice == "2":
            res, trace = subtract(a, b)
            print("\n" + format_subtraction_conta_armada(trace))
            print(f"\nResultado Final: {res.to_string()} (Base {base})")
        else:
            print("Opção inválida.")
    except Exception as e:
        print(f"\n[ERRO]: {e}")


def menu_conversao():
    print("\n--- MENU: CONVERSÃO DIRETA ENTRE BASES ---")
    try:
        source_base = int(input("Informe a base de ORIGEM (2 a 36): ").strip())
        num_str = input(f"Informe o número na base de origem ({source_base}): ").strip()
        target_base = int(input("Informe a base de DESTINO (2 a 36): ").strip())

        number = BaseNumber.from_string(num_str, source_base)
        print(f"\nConvertendo {number.to_string()} (base {source_base}) para a base {target_base}...")
        res = convert(number, target_base)
        print("\n" + format_conversion_report(res))
    except Exception as e:
        print(f"\n[ERRO]: {e}")


def menu_exemplos():
    print("\n--- DEMONSTRAÇÕES E CASOS CLÁSSICOS ---")
    print("1. Adição Hexadecimal com múltiplos carries: 1F.8 + 0.C")
    a = BaseNumber.from_string("1F.8", 16)
    b = BaseNumber.from_string("0.C", 16)
    _, trace_add = add(a, b)
    print(format_addition_conta_armada(trace_add))

    print("\n" + "=" * 60 + "\n")
    print("2. Subtração com empréstimos múltiplos em cascata: 100.2 - 0.7 na base 8")
    c = BaseNumber.from_string("100.2", 8)
    d = BaseNumber.from_string("0.7", 8)
    _, trace_sub = subtract(c, d)
    print(format_subtraction_conta_armada(trace_sub))

    print("\n" + "=" * 60 + "\n")
    print("3. Conversão de Real sem pivô decimal com Dízima Periódica Nativa: (0.12)_4 para Base 3")
    orig = BaseNumber.from_string("0.12", 4)
    conv_res = convert(orig, 3)
    print(format_conversion_report(conv_res))

    print("\n" + "=" * 60 + "\n")
    print("4. Conversão clássica do IEEE 754: 0.1 na Base 10 para Binário (Base 2)")
    orig_dec = BaseNumber.from_string("0.1", 10)
    conv_bin = convert(orig_dec, 2)
    print(format_conversion_report(conv_bin))


def run_tests():
    import unittest
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def main():
    banner()
    while True:
        print("\n" + "=" * 45)
        print("          MENU PRINCIPAL")
        print("=" * 45)
        print("1. Operações Elementares (Adição e Subtração)")
        print("2. Conversão Direta de Bases (Reais e Dízimas)")
        print("3. Demonstrações e Casos Didáticos")
        print("4. Executar Bateria de Testes")
        print("5. Sair")
        print("=" * 45)

        choice = input("Escolha uma opção (1-5): ").strip()

        if choice == "1":
            menu_operacoes()
        elif choice == "2":
            menu_conversao()
        elif choice == "3":
            menu_exemplos()
        elif choice == "4":
            run_tests()
        elif choice == "5":
            print("\nEncerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
