"""
Módulo de Conversão entre Bases Arbitrárias.
Utiliza aritmética polinomial calculada na base de origem ou de destino,
sem coerção para a base decimal ou para tipos primitivos float do IEEE 754.
Detecta dízimas periódicas nativas a partir do histórico de restos fracionários.
"""

from typing import Dict, List, Optional, Tuple
from src.alphabet import value_to_char, validate_base
from src.base_number import BaseNumber
from src.operations import add, scalar_multiply


class ConversionResult:
    """Armazena o resultado e o relatório de execução da conversão direta."""

    def __init__(
        self,
        source_number: BaseNumber,
        target_base: int,
        result_number: BaseNumber,
        integer_steps: List[str],
        fractional_steps: List[str],
        is_periodic: bool = False,
        period_start: Optional[int] = None,
        period_length: Optional[int] = None,
    ):
        self.source_number = source_number
        self.target_base = target_base
        self.result_number = result_number
        self.integer_steps = integer_steps
        self.fractional_steps = fractional_steps
        self.is_periodic = is_periodic
        self.period_start = period_start
        self.period_length = period_length


def _int_value_of_digits(digits: List[int], base: int) -> int:
    """
    Avalia o valor numérico de um vetor de dígitos inteiros.
    Utilizado para mapear o overflow de vírgula (< target_base) para um dígito isolado.
    """
    val = 0
    for d in digits:
        val = val * base + d
    return val


def _convert_integer_part_horner(
    int_digits: List[int], source_base: int, target_base: int
) -> Tuple[List[int], List[str]]:
    """
    Converte a parte inteira usando o Algoritmo de Horner calculado na base de destino.
    P = (...((d_k * B_orig + d_{k-1}) * B_orig + ...) + d_0
    Cada multiplicação e adição é executada via BaseNumber na base de destino.
    """
    steps = []
    # Acumulador P = 0 na base de destino
    acc = BaseNumber(
        base=target_base,
        sign=1,
        integer_digits=[0],
        fractional_digits=[],
    )

    steps.append(
        f"Inicialização do acumulador na base de destino ({target_base}): P = {acc.to_string()}"
    )

    for idx, d_orig in enumerate(int_digits):
        pos = len(int_digits) - 1 - idx
        # Converte o dígito da base de origem para um BaseNumber na base de destino
        # d_orig é um valor entre 0 e source_base - 1
        d_target_digits = []
        temp_val = d_orig
        if temp_val == 0:
            d_target_digits = [0]
        else:
            while temp_val > 0:
                d_target_digits.insert(0, temp_val % target_base)
                temp_val //= target_base

        d_num = BaseNumber(
            base=target_base,
            sign=1,
            integer_digits=d_target_digits,
            fractional_digits=[],
        )

        char_orig = value_to_char(d_orig, source_base)
        step_str = (
            f"Passo {idx + 1} (dígito de peso {source_base}^{pos} = '{char_orig}' [valor {d_orig}]): "
            f"P = (P * {source_base}) + {d_num.to_string()}"
        )

        # Multiplica o acumulador atual por source_base na base de destino
        # via soma repetida (aritmética na base target_base)
        acc_scaled = scalar_multiply(acc, source_base)

        # Adiciona o dígito atual
        acc, _ = add(acc_scaled, d_num)

        step_str += f" => P = {acc.to_string()}"
        steps.append(step_str)

    return acc.integer_digits, steps


def _convert_fractional_part(
    frac_digits: List[int],
    source_base: int,
    target_base: int,
    max_digits: int = 50,
) -> Tuple[List[int], Optional[int], bool, List[str]]:
    """
    Converte a parte fracionária utilizando multiplicações sucessivas por target_base
    executadas na base de origem.
    Rastreia o histórico de estados fracionários para detectar dízimas periódicas nativas.
    """
    steps = []
    if not frac_digits or all(d == 0 for d in frac_digits):
        return [], None, False, ["Parte fracionária nula; conversão direta imediata."]

    # Estado fracionário inicial em source_base
    current_frac = BaseNumber(
        base=source_base,
        sign=1,
        integer_digits=[0],
        fractional_digits=list(frac_digits),
    )
    current_frac.normalize()

    history: Dict[Tuple[int, ...], int] = {}
    target_digits: List[int] = []
    repeating_start: Optional[int] = None
    is_periodic = False

    steps.append(
        f"Início da conversão fracionária: Fração inicial = 0.{current_frac.to_string().split('.')[-1]} "
        f"na base {source_base}. Multiplicador = base de destino ({target_base})."
    )

    iteration = 0
    while iteration < max_digits:
        frac_tuple = tuple(current_frac.fractional_digits)

        # 1. Se a fração zerou, a representação é exata e finita
        if not frac_tuple or all(d == 0 for d in frac_tuple):
            steps.append(
                f"Passo {iteration + 1}: Resto fracionário zerou. Representação finita e exata na base {target_base}."
            )
            break

        # 2. Se a fração já foi vista anteriormente, detectamos um ciclo perfeito (dízima periódica)
        if frac_tuple in history:
            repeating_start = history[frac_tuple]
            is_periodic = True
            period_len = len(target_digits) - repeating_start
            period_syms = "".join(
                value_to_char(target_digits[k], target_base)
                for k in range(repeating_start, len(target_digits))
            )
            steps.append(
                f"Passo {iteration + 1}: Estado fracionário {frac_tuple} já ocorreu no passo {repeating_start + 1}. "
                f"Dízima periódica nativa detectada! Período de tamanho {period_len}: ({period_syms})."
            )
            break

        history[frac_tuple] = len(target_digits)

        # Multiplica a fração atual por target_base na base de origem (source_base)
        product = scalar_multiply(current_frac, target_base)

        # O que transbordou para a parte inteira é o dígito gerado na base de destino
        overflow_val = _int_value_of_digits(product.integer_digits, source_base)
        if overflow_val >= target_base:
            raise RuntimeError(
                f"Erro algorítmico: transbordo ({overflow_val}) maior ou igual à base de destino ({target_base})."
            )

        target_digits.append(overflow_val)
        target_char = value_to_char(overflow_val, target_base)

        # Nova fração restante na base de origem
        current_frac = BaseNumber(
            base=source_base,
            sign=1,
            integer_digits=[0],
            fractional_digits=product.fractional_digits,
        )
        current_frac.normalize()

        frac_str = "".join(
            value_to_char(d, source_base) for d in current_frac.fractional_digits
        )
        steps.append(
            f"Passo {iteration + 1}: Fração atual * {target_base} = {product.to_string()} (base {source_base}) "
            f"-> Dígito extraído: '{target_char}' (valor {overflow_val}), Nova fração restante: 0.{frac_str or '0'}"
        )

        iteration += 1

    if iteration >= max_digits and not is_periodic and current_frac.fractional_digits:
        steps.append(
            f"Limite máximo de precisão ({max_digits} dígitos) atingido sem fechamento de ciclo."
        )

    return target_digits, repeating_start, is_periodic, steps


def convert(
    number: BaseNumber,
    target_base: int,
    max_fraction_digits: int = 50,
) -> ConversionResult:
    """
    Realiza a conversão direta de um número real entre bases arbitrárias:
    - Parte inteira convertida via Horner na base de destino.
    - Parte fracionária convertida via multiplicações sucessivas na base de origem.
    - Sem coerção decimal ou binária intermediária.
    - Detecção de dízimas periódicas.
    """
    validate_base(target_base)

    if number.base == target_base:
        return ConversionResult(
            source_number=number,
            target_base=target_base,
            result_number=number.copy(),
            integer_steps=[
                "Bases de origem e destino idênticas; nenhuma conversão necessária."
            ],
            fractional_steps=[],
            is_periodic=number.repeating_start is not None,
            period_start=number.repeating_start,
            period_length=(
                len(number.fractional_digits) - number.repeating_start
                if number.repeating_start is not None
                else None
            ),
        )

    # 1. Conversão da parte inteira
    int_digits_res, int_steps = _convert_integer_part_horner(
        number.integer_digits, number.base, target_base
    )

    # 2. Conversão da parte fracionária
    frac_digits_res, rep_start, is_periodic, frac_steps = _convert_fractional_part(
        number.fractional_digits,
        number.base,
        target_base,
        max_digits=max_fraction_digits,
    )

    result_num = BaseNumber(
        base=target_base,
        sign=number.sign,
        integer_digits=int_digits_res,
        fractional_digits=frac_digits_res,
        repeating_start=rep_start,
    )

    period_len = None
    if rep_start is not None:
        period_len = len(frac_digits_res) - rep_start

    return ConversionResult(
        source_number=number,
        target_base=target_base,
        result_number=result_num,
        integer_steps=int_steps,
        fractional_steps=frac_steps,
        is_periodic=is_periodic,
        period_start=rep_start,
        period_length=period_len,
    )
