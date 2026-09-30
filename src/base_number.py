"""
Módulo da Estrutura Vetorial de Números em Bases Arbitrárias.
Substitui tipos primitivos de ponto flutuante de máquina por vetores de dígitos isolados,
evitando qualquer coerção para decimal ou binário IEEE 754.
"""

from typing import List, Optional
from src.alphabet import validate_base, char_to_value, value_to_char


class BaseNumber:
    """
    Representação estruturada de um número real em base arbitrária (2 a 36).
    Armazena o sinal e vetores de inteiros com os valores dos dígitos posicionais.
    """

    def __init__(
        self,
        base: int,
        sign: int = 1,
        integer_digits: Optional[List[int]] = None,
        fractional_digits: Optional[List[int]] = None,
        repeating_start: Optional[int] = None,
    ):
        validate_base(base)
        self.base = base
        self.sign = -1 if sign < 0 else 1
        self.integer_digits: List[int] = (
            list(integer_digits) if integer_digits is not None else [0]
        )
        self.fractional_digits: List[int] = (
            list(fractional_digits) if fractional_digits is not None else []
        )
        self.repeating_start: Optional[int] = repeating_start

        self._validate_digits()
        self.normalize()

    def _validate_digits(self) -> None:
        """Verifica se todos os dígitos estão dentro dos limites da base."""
        for d in self.integer_digits:
            if not isinstance(d, int) or d < 0 or d >= self.base:
                raise ValueError(
                    f"Dígito inteiro inválido {d} para a base {self.base}."
                )
        for d in self.fractional_digits:
            if not isinstance(d, int) or d < 0 or d >= self.base:
                raise ValueError(
                    f"Dígito fracionário inválido {d} para a base {self.base}."
                )
        if self.repeating_start is not None:
            if self.repeating_start < 0 or self.repeating_start >= len(
                self.fractional_digits
            ):
                raise ValueError(
                    f"Índice de início da dízima ({self.repeating_start}) fora do intervalo de dígitos fracionários."
                )

    def normalize(self) -> "BaseNumber":
        """
        Normaliza a representação:
        - Remove zeros à esquerda na parte inteira (mantendo ao menos um dígito [0]).
        - Remove zeros à direita na parte fracionária se não for dízima periódica.
        - Se o valor for 0, o sinal torna-se positivo (+1).
        """
        while len(self.integer_digits) > 1 and self.integer_digits[0] == 0:
            self.integer_digits.pop(0)
        if not self.integer_digits:
            self.integer_digits = [0]

        if self.repeating_start is None:
            while self.fractional_digits and self.fractional_digits[-1] == 0:
                self.fractional_digits.pop()

        if self.is_zero():
            self.sign = 1
            if self.repeating_start is not None and all(
                d == 0 for d in self.fractional_digits
            ):
                self.fractional_digits = []
                self.repeating_start = None

        return self

    def is_zero(self) -> bool:
        """Retorna True se o número for exatamente zero."""
        return all(d == 0 for d in self.integer_digits) and all(
            d == 0 for d in self.fractional_digits
        )

    def copy(self) -> "BaseNumber":
        """Cria uma cópia profunda da estrutura."""
        return BaseNumber(
            base=self.base,
            sign=self.sign,
            integer_digits=self.integer_digits.copy(),
            fractional_digits=self.fractional_digits.copy(),
            repeating_start=self.repeating_start,
        )

    def abs_compare(self, other: "BaseNumber") -> int:
        """
        Compara o valor absoluto (|self| vs |other|).
        Retorna:
          1 se |self| > |other|
         -1 se |self| < |other|
          0 se |self| == |other|
        """
        if self.base != other.base:
            raise ValueError(
                f"Comparação permitida apenas entre números de mesma base ({self.base} != {other.base})"
            )

        # 1. Comparar tamanho da parte inteira normalizada
        len1 = len(self.integer_digits)
        len2 = len(other.integer_digits)
        if len1 > len2:
            return 1
        if len1 < len2:
            return -1

        # 2. Comparar dígitos inteiros da esquerda para a direita
        for d1, d2 in zip(self.integer_digits, other.integer_digits):
            if d1 > d2:
                return 1
            if d1 < d2:
                return -1

        # 3. Comparar dígitos fracionários
        max_frac = max(len(self.fractional_digits), len(other.fractional_digits))
        for i in range(max_frac):
            d1 = self.fractional_digits[i] if i < len(self.fractional_digits) else 0
            d2 = other.fractional_digits[i] if i < len(other.fractional_digits) else 0
            if d1 > d2:
                return 1
            if d1 < d2:
                return -1

        return 0

    @classmethod
    def from_string(cls, text: str, base: int) -> "BaseNumber":
        """
        Interpreta uma string representando um número na base dada.
        Suporta formatos:
          - "-1A.3F"
          - "+0.125"
          - "3,14" (vírgula como separador)
          - "0.1(012)" para dízimas periódicas nativas.
        """
        text = text.strip()
        if not text:
            raise ValueError("String vazia não pode ser convertida para BaseNumber.")

        sign = 1
        if text.startswith("-"):
            sign = -1
            text = text[1:].strip()
        elif text.startswith("+"):
            text = text[1:].strip()

        text = text.replace(",", ".")

        if "." in text:
            parts = text.split(".", 1)
            int_str = parts[0]
            frac_str = parts[1]
        else:
            int_str = text
            frac_str = ""

        int_digits = []
        if int_str:
            for ch in int_str:
                int_digits.append(char_to_value(ch, base))
        else:
            int_digits = [0]

        frac_digits = []
        repeating_start = None

        if frac_str:
            if "(" in frac_str and ")" in frac_str:
                pre, rest = frac_str.split("(", 1)
                periodic = rest.split(")", 1)[0]
                for ch in pre:
                    frac_digits.append(char_to_value(ch, base))
                repeating_start = len(frac_digits)
                for ch in periodic:
                    frac_digits.append(char_to_value(ch, base))
            else:
                for ch in frac_str:
                    frac_digits.append(char_to_value(ch, base))

        return cls(
            base=base,
            sign=sign,
            integer_digits=int_digits,
            fractional_digits=frac_digits,
            repeating_start=repeating_start,
        )

    def to_string(self) -> str:
        """
        Formata o número em string representativa (0-9, A-Z).
        Dízimas periódicas são representadas com parênteses, ex: 0.1(012).
        """
        sign_str = "-" if self.sign < 0 and not self.is_zero() else ""
        int_str = "".join(value_to_char(d, self.base) for d in self.integer_digits)

        if not self.fractional_digits:
            return f"{sign_str}{int_str}"

        if self.repeating_start is not None:
            pre_digits = self.fractional_digits[: self.repeating_start]
            per_digits = self.fractional_digits[self.repeating_start :]
            pre_str = "".join(value_to_char(d, self.base) for d in pre_digits)
            per_str = "".join(value_to_char(d, self.base) for d in per_digits)
            return f"{sign_str}{int_str}.{pre_str}({per_str})"
        else:
            frac_str = "".join(value_to_char(d, self.base) for d in self.fractional_digits)
            return f"{sign_str}{int_str}.{frac_str}"

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f"BaseNumber({self.to_string()}, base={self.base})"
