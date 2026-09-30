"""
Módulo de Mapeamento de Caracteres e Validação de Bases.
Suporta dígitos e letras padrão (0-9, A-Z) para bases de 2 a 36.
"""

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_base(base: int) -> None:
    """Verifica se a base informada é um inteiro válido entre 2 e 36."""
    if not isinstance(base, int):
        raise TypeError(f"A base deve ser um número inteiro, recebido: {type(base).__name__}")
    if base < 2 or base > 36:
        raise ValueError(f"Base inválida ({base}). O sistema suporta bases de 2 a 36.")


def char_to_value(char: str, base: int) -> int:
    """Converte um caractere alfanumérico para seu valor inteiro na base dada."""
    validate_base(base)
    upper_char = char.upper()
    if upper_char not in DIGITS:
        raise ValueError(f"Caractere '{char}' não é um símbolo alfanumérico válido.")
    val = DIGITS.index(upper_char)
    if val >= base:
        raise ValueError(
            f"Dígito '{char}' (valor {val}) é inválido para a base {base} (válidos: 0 a {DIGITS[base - 1]})."
        )
    return val


def value_to_char(val: int, base: int) -> str:
    """Converte um valor numérico inteiro para o caractere representativo na base dada."""
    validate_base(base)
    if not isinstance(val, int):
        raise TypeError(f"O valor deve ser inteiro, recebido: {type(val).__name__}")
    if val < 0 or val >= base:
        raise ValueError(f"Valor {val} fora dos limites válidos para a base {base} [0, {base - 1}].")
    return DIGITS[val]
