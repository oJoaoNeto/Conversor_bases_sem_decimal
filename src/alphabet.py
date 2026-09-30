"""
Módulo de Gerenciamento de Alfabetos e Mapeamento de Dígitos.
Suporta bases posicionais arbitrárias de 2 a 36 por padrão (0-9, A-Z),
com capacidade de extensão para conjuntos de caracteres customizados.
"""

from typing import Optional

DEFAULT_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Alphabet:
    """
    Controla o mapeamento entre caracteres visuais e valores numéricos inteiros isolados.
    """

    def __init__(self, symbols: str = DEFAULT_DIGITS):
        if len(symbols) < 2:
            raise ValueError("O alfabeto deve possuir no mínimo 2 símbolos.")
        if len(set(symbols)) != len(symbols):
            raise ValueError("Símbolos duplicados no alfabeto não são permitidos.")
        self.symbols = symbols
        self.char_to_val_map = {ch: i for i, ch in enumerate(symbols)}
        self.val_to_char_map = {i: ch for i, ch in enumerate(symbols)}
        self.max_supported_base = len(symbols)

    def validate_base(self, base: int) -> None:
        """Verifica se a base está dentro do intervalo suportado."""
        if not isinstance(base, int):
            raise TypeError(f"A base deve ser um número inteiro, recebido: {type(base).__name__}")
        if base < 2:
            raise ValueError(f"A base deve ser maior ou igual a 2. Recebido: {base}")
        if base > self.max_supported_base:
            raise ValueError(
                f"Base {base} excede o limite suportado pelo alfabeto atual ({self.max_supported_base})."
            )

    def char_to_value(self, char: str, base: int) -> int:
        """Converte um caractere para seu valor numérico na base dada."""
        self.validate_base(base)
        upper_char = char.upper()
        if upper_char not in self.char_to_val_map:
            raise ValueError(f"Caractere '{char}' não reconhecido no alfabeto.")
        val = self.char_to_val_map[upper_char]
        if val >= base:
            raise ValueError(
                f"Dígito '{char}' (valor {val}) é inválido para a base {base} (dígitos válidos: 0 a {self.val_to_char_map[base - 1]})."
            )
        return val

    def value_to_char(self, val: int, base: int) -> str:
        """Converte um valor numérico para o caractere representativo na base dada."""
        self.validate_base(base)
        if not isinstance(val, int):
            raise TypeError(f"O valor deve ser inteiro, recebido: {type(val).__name__}")
        if val < 0 or val >= base:
            raise ValueError(f"Valor {val} fora dos limites válidos para a base {base} [0, {base - 1}].")
        return self.val_to_char_map[val]


# Instância global padrão do alfabeto
default_alphabet = Alphabet()
