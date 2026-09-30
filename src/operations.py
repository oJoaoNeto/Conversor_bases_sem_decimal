"""
Módulo de Operações Elementares: Adição e Subtração em Base Arbitrária.
Executa cálculos coluna a coluna manipulando vetores de dígitos,
com rastreio completo de 'vai-um' (carry) e 'empresta-um' (borrow)
para renderização de contas armadas fiéis.
"""

from typing import List, Optional, Tuple
from src.base_number import BaseNumber


class AdditionTrace:
    """Registra todos os passos intermediários da adição para a conta armada."""

    def __init__(
        self,
        operand_a: BaseNumber,
        operand_b: BaseNumber,
        result: BaseNumber,
        aligned_a_int: List[int],
        aligned_b_int: List[int],
        aligned_a_frac: List[int],
        aligned_b_frac: List[int],
        carries_int: List[int],
        carries_frac: List[int],
        steps: List[str],
    ):
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.result = result
        self.aligned_a_int = aligned_a_int
        self.aligned_b_int = aligned_b_int
        self.aligned_a_frac = aligned_a_frac
        self.aligned_b_frac = aligned_b_frac
        self.carries_int = carries_int
        self.carries_frac = carries_frac
        self.steps = steps


class SubtractionTrace:
    """Registra todos os passos intermediários da subtração para a conta armada."""

    def __init__(
        self,
        operand_a: BaseNumber,
        operand_b: BaseNumber,
        result: BaseNumber,
        aligned_a_int: List[int],
        aligned_b_int: List[int],
        aligned_a_frac: List[int],
        aligned_b_frac: List[int],
        borrows_int: List[int],
        borrows_frac: List[int],
        steps: List[str],
        swapped_operands: bool = False,
    ):
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.result = result
        self.aligned_a_int = aligned_a_int
        self.aligned_b_int = aligned_b_int
        self.aligned_a_frac = aligned_a_frac
        self.aligned_b_frac = aligned_b_frac
        self.borrows_int = borrows_int
        self.borrows_frac = borrows_frac
        self.steps = steps
        self.swapped_operands = swapped_operands


def _align_operands(
    a: BaseNumber, b: BaseNumber
) -> Tuple[List[int], List[int], List[int], List[int]]:
    """
    Alinha os dígitos inteiros e fracionários de dois números preenchendo com zeros.
    Retorna (a_int, b_int, a_frac, b_frac).
    """
    max_int = max(len(a.integer_digits), len(b.integer_digits))
    max_frac = max(len(a.fractional_digits), len(b.fractional_digits))

    a_int = [0] * (max_int - len(a.integer_digits)) + list(a.integer_digits)
    b_int = [0] * (max_int - len(b.integer_digits)) + list(b.integer_digits)

    a_frac = list(a.fractional_digits) + [0] * (max_frac - len(a.fractional_digits))
    b_frac = list(b.fractional_digits) + [0] * (max_frac - len(b.fractional_digits))

    return a_int, b_int, a_frac, b_frac


def _raw_magnitude_add(
    a: BaseNumber, b: BaseNumber
) -> Tuple[List[int], List[int], List[int], List[int], List[int], List[int], List[str]]:
    """
    Soma estrita de magnitudes (|a| + |b|) na base dada.
    Retorna (res_int, res_frac, carries_int, carries_frac, a_int, b_int, steps).
    """
    base = a.base
    alphabet = a.alphabet
    a_int, b_int, a_frac, b_frac = _align_operands(a, b)

    carries_frac = [0] * len(a_frac)
    res_frac = [0] * len(a_frac)
    steps = []

    carry = 0
    # 1. Soma da parte fracionária (da direita para a esquerda)
    for i in range(len(a_frac) - 1, -1, -1):
        da, db = a_frac[i], b_frac[i]
        total = da + db + carry
        new_digit = total % base
        new_carry = total // base
        res_frac[i] = new_digit
        carries_frac[i] = carry

        step_desc = (
            f"Fracionário col {i+1}: {alphabet.value_to_char(da, base)} ({da}) + "
            f"{alphabet.value_to_char(db, base)} ({db})"
        )
        if carry > 0:
            step_desc += f" + vai-um ({carry})"
        step_desc += (
            f" = {total} -> Dígito: {alphabet.value_to_char(new_digit, base)} ({new_digit}), "
            f"Novo vai-um: {new_carry}"
        )
        steps.append(step_desc)
        carry = new_carry

    # 2. Soma da parte inteira (da direita para a esquerda)
    n_int = len(a_int)
    carries_int = [0] * n_int
    res_int = [0] * n_int

    for i in range(n_int - 1, -1, -1):
        da, db = a_int[i], b_int[i]
        total = da + db + carry
        new_digit = total % base
        new_carry = total // base
        res_int[i] = new_digit
        carries_int[i] = carry

        col_pos = n_int - 1 - i
        step_desc = (
            f"Inteiro col {col_pos}: {alphabet.value_to_char(da, base)} ({da}) + "
            f"{alphabet.value_to_char(db, base)} ({db})"
        )
        if carry > 0:
            step_desc += f" + vai-um ({carry})"
        step_desc += (
            f" = {total} -> Dígito: {alphabet.value_to_char(new_digit, base)} ({new_digit}), "
            f"Novo vai-um: {new_carry}"
        )
        steps.append(step_desc)
        carry = new_carry

    # Se sobrou carry no dígito mais significativo
    final_carries_int = list(carries_int)
    if carry > 0:
        res_int.insert(0, carry)
        final_carries_int.insert(0, carry)
        steps.append(
            f"Carry final transbordado para a esquerda: {alphabet.value_to_char(carry, base)} ({carry})"
        )

    return res_int, res_frac, final_carries_int, carries_frac, steps


def _raw_magnitude_subtract(
    big: BaseNumber, small: BaseNumber
) -> Tuple[List[int], List[int], List[int], List[int], List[str]]:
    """
    Subtração de magnitudes (|big| - |small| com |big| >= |small|).
    Retorna (res_int, res_frac, borrows_int, borrows_frac, steps).
    """
    base = big.base
    alphabet = big.alphabet
    b_int, s_int, b_frac, s_frac = _align_operands(big, small)

    borrows_frac = [0] * len(b_frac)
    res_frac = [0] * len(b_frac)
    steps = []

    borrow = 0
    # 1. Subtração fracionária (da direita para a esquerda)
    for i in range(len(b_frac) - 1, -1, -1):
        db = b_frac[i]
        ds = s_frac[i]
        current_borrow = borrow
        borrows_frac[i] = current_borrow

        effective_db = db - current_borrow
        if effective_db < ds:
            effective_db += base
            new_borrow = 1
        else:
            new_borrow = 0

        diff = effective_db - ds
        res_frac[i] = diff

        step_desc = (
            f"Fracionário col {i+1}: {alphabet.value_to_char(db, base)} ({db})"
        )
        if current_borrow > 0:
            step_desc += f" - empresta ({current_borrow})"
        if new_borrow > 0:
            step_desc += f" + base ({base}) [pediu emprestado]"
        step_desc += (
            f" - {alphabet.value_to_char(ds, base)} ({ds}) = "
            f"{alphabet.value_to_char(diff, base)} ({diff})"
        )
        steps.append(step_desc)
        borrow = new_borrow

    # 2. Subtração inteira (da direita para a esquerda)
    n_int = len(b_int)
    borrows_int = [0] * n_int
    res_int = [0] * n_int

    for i in range(n_int - 1, -1, -1):
        db = b_int[i]
        ds = s_int[i]
        current_borrow = borrow
        borrows_int[i] = current_borrow

        effective_db = db - current_borrow
        if effective_db < ds:
            effective_db += base
            new_borrow = 1
        else:
            new_borrow = 0

        diff = effective_db - ds
        res_int[i] = diff

        col_pos = n_int - 1 - i
        step_desc = (
            f"Inteiro col {col_pos}: {alphabet.value_to_char(db, base)} ({db})"
        )
        if current_borrow > 0:
            step_desc += f" - empresta ({current_borrow})"
        if new_borrow > 0:
            step_desc += f" + base ({base}) [pediu emprestado]"
        step_desc += (
            f" - {alphabet.value_to_char(ds, base)} ({ds}) = "
            f"{alphabet.value_to_char(diff, base)} ({diff})"
        )
        steps.append(step_desc)
        borrow = new_borrow

    return res_int, res_frac, borrows_int, borrows_frac, steps


def add(a: BaseNumber, b: BaseNumber) -> Tuple[BaseNumber, AdditionTrace]:
    """
    Soma algébrica de dois números em base arbitrária: a + b.
    Trata sinais opostos desviando para subtração de magnitudes quando necessário.
    Retorna o resultado como BaseNumber e a estrutura de rastreio para conta armada.
    """
    if a.base != b.base:
        raise ValueError(f"As bases devem ser iguais para a soma: {a.base} != {b.base}")

    base = a.base
    a_int, b_int, a_frac, b_frac = _align_operands(a, b)

    # Caso 1: Sinais iguais (ambos positivos ou ambos negativos)
    if a.sign == b.sign:
        res_int, res_frac, carries_int, carries_frac, steps = _raw_magnitude_add(a, b)
        result = BaseNumber(
            base=base,
            sign=a.sign,
            integer_digits=res_int,
            fractional_digits=res_frac,
            alphabet=a.alphabet,
        )
        trace = AdditionTrace(
            operand_a=a,
            operand_b=b,
            result=result,
            aligned_a_int=a_int,
            aligned_b_int=b_int,
            aligned_a_frac=a_frac,
            aligned_b_frac=b_frac,
            carries_int=carries_int,
            carries_frac=carries_frac,
            steps=steps,
        )
        return result, trace

    # Caso 2: Sinais opostos (a + (-b) ou (-a) + b) -> vira subtração de magnitudes
    cmp = a.abs_compare(b)
    if cmp == 0:
        # Resultado é exatamente 0
        result = BaseNumber(base=base, sign=1, integer_digits=[0], fractional_digits=[], alphabet=a.alphabet)
        trace = AdditionTrace(
            operand_a=a,
            operand_b=b,
            result=result,
            aligned_a_int=a_int,
            aligned_b_int=b_int,
            aligned_a_frac=a_frac,
            aligned_b_frac=b_frac,
            carries_int=[0] * len(a_int),
            carries_frac=[0] * len(a_frac),
            steps=["Valores absolutos idênticos com sinais opostos: resultado é zero."],
        )
        return result, trace
    elif cmp > 0:
        # |a| > |b|: sinal é o de 'a'
        res_int, res_frac, borrows_int, borrows_frac, steps = _raw_magnitude_subtract(a, b)
        result = BaseNumber(
            base=base,
            sign=a.sign,
            integer_digits=res_int,
            fractional_digits=res_frac,
            alphabet=a.alphabet,
        )
        trace = AdditionTrace(
            operand_a=a,
            operand_b=b,
            result=result,
            aligned_a_int=a_int,
            aligned_b_int=b_int,
            aligned_a_frac=a_frac,
            aligned_b_frac=b_frac,
            carries_int=borrows_int,
            carries_frac=borrows_frac,
            steps=[f"Sinais opostos com |A| > |B|. Efetuada subtração |A| - |B|:"] + steps,
        )
        return result, trace
    else:
        # |a| < |b|: sinal é o de 'b'
        res_int, res_frac, borrows_int, borrows_frac, steps = _raw_magnitude_subtract(b, a)
        result = BaseNumber(
            base=base,
            sign=b.sign,
            integer_digits=res_int,
            fractional_digits=res_frac,
            alphabet=a.alphabet,
        )
        trace = AdditionTrace(
            operand_a=a,
            operand_b=b,
            result=result,
            aligned_a_int=a_int,
            aligned_b_int=b_int,
            aligned_a_frac=a_frac,
            aligned_b_frac=b_frac,
            carries_int=borrows_int,
            carries_frac=borrows_frac,
            steps=[f"Sinais opostos com |A| < |B|. Efetuada subtração |B| - |A|:"] + steps,
        )
        return result, trace


def subtract(a: BaseNumber, b: BaseNumber) -> Tuple[BaseNumber, SubtractionTrace]:
    """
    Subtração algébrica de dois números em base arbitrária: a - b.
    Retorna o resultado como BaseNumber e a estrutura de rastreio para conta armada.
    """
    if a.base != b.base:
        raise ValueError(f"As bases devem ser iguais para a subtração: {a.base} != {b.base}")

    base = a.base
    a_int, b_int, a_frac, b_frac = _align_operands(a, b)

    # Caso direto: Ambos positivos e a >= b
    if a.sign > 0 and b.sign > 0:
        cmp = a.abs_compare(b)
        if cmp >= 0:
            res_int, res_frac, borrows_int, borrows_frac, steps = _raw_magnitude_subtract(a, b)
            result = BaseNumber(
                base=base,
                sign=1,
                integer_digits=res_int,
                fractional_digits=res_frac,
                alphabet=a.alphabet,
            )
            trace = SubtractionTrace(
                operand_a=a,
                operand_b=b,
                result=result,
                aligned_a_int=a_int,
                aligned_b_int=b_int,
                aligned_a_frac=a_frac,
                aligned_b_frac=b_frac,
                borrows_int=borrows_int,
                borrows_frac=borrows_frac,
                steps=steps,
                swapped_operands=False,
            )
            return result, trace
        else:
            # a < b => -(b - a)
            b_int_swp, a_int_swp, b_frac_swp, a_frac_swp = _align_operands(b, a)
            res_int, res_frac, borrows_int, borrows_frac, steps = _raw_magnitude_subtract(b, a)
            result = BaseNumber(
                base=base,
                sign=-1,
                integer_digits=res_int,
                fractional_digits=res_frac,
                alphabet=a.alphabet,
            )
            trace = SubtractionTrace(
                operand_a=a,
                operand_b=b,
                result=result,
                aligned_a_int=b_int_swp,
                aligned_b_int=a_int_swp,
                aligned_a_frac=b_frac_swp,
                aligned_b_frac=a_frac_swp,
                borrows_int=borrows_int,
                borrows_frac=borrows_frac,
                steps=["Como A < B, armou-se |B| - |A| e o resultado recebeu sinal negativo:"] + steps,
                swapped_operands=True,
            )
            return result, trace

    # Caso geral de sinais: a - b = a + (-b)
    b_neg = b.copy()
    b_neg.sign = -b.sign
    res_add, add_trace = add(a, b_neg)

    # Gera um trace adaptado
    trace = SubtractionTrace(
        operand_a=a,
        operand_b=b,
        result=res_add,
        aligned_a_int=a_int,
        aligned_b_int=b_int,
        aligned_a_frac=a_frac,
        aligned_b_frac=b_frac,
        borrows_int=add_trace.carries_int,
        borrows_frac=add_trace.carries_frac,
        steps=[f"Aritmética com sinais: A - B calculado como A + (-B)."] + add_trace.steps,
    )
    return res_add, trace


def scalar_multiply(num: BaseNumber, scalar: int) -> BaseNumber:
    """
    Multiplica um BaseNumber por um inteiro escalar >= 0 na mesma base,
    utilizando estritamente adição sucessiva baseada em BaseNumber.
    Não utiliza coerção decimal nem ponto flutuante de máquina.
    """
    if scalar < 0:
        raise ValueError("Escalar deve ser não-negativo.")
    if scalar == 0 or num.is_zero():
        return BaseNumber(base=num.base, sign=1, integer_digits=[0], fractional_digits=[], alphabet=num.alphabet)
    if scalar == 1:
        return num.copy()

    # Algoritmo de duplicação e soma (double-and-add) usando a própria função add
    res = BaseNumber(base=num.base, sign=1, integer_digits=[0], fractional_digits=[], alphabet=num.alphabet)
    current = num.copy()
    current.sign = 1  # magnitude

    k = scalar
    while k > 0:
        if k % 2 == 1:
            res, _ = add(res, current)
        if k > 1:
            current, _ = add(current, current)
        k //= 2

    res.sign = num.sign
    return res
