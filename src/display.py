"""
Módulo de Visualização e Renderização em Terminal.
Responsável por formatar contas de Adição e Subtração,
com exibição de vai-um (carry) e empresta-um (borrow),
além de formatar o passo a passo da conversão direta de bases.
"""

from src.alphabet import value_to_char
from src.operations import AdditionTrace, SubtractionTrace
from src.converter import ConversionResult


def format_addition_conta_armada(trace: AdditionTrace) -> str:
    """Formata visualmente a conta da adição com alinhamento e linha de vai-um."""
    base = trace.operand_a.base

    a_int_str = "".join(value_to_char(d, base) for d in trace.aligned_a_int)
    b_int_str = "".join(value_to_char(d, base) for d in trace.aligned_b_int)

    has_frac = len(trace.aligned_a_frac) > 0
    a_frac_str = (
        "".join(value_to_char(d, base) for d in trace.aligned_a_frac)
        if has_frac
        else ""
    )
    b_frac_str = (
        "".join(value_to_char(d, base) for d in trace.aligned_b_frac)
        if has_frac
        else ""
    )

    # Linha de vai-um (carries)
    carries_int_syms = [
        str(c) if c > 0 else " " for c in trace.carries_int[-len(trace.aligned_a_int) :]
    ]
    carries_frac_syms = [str(c) if c > 0 else " " for c in trace.carries_frac]

    carry_int_str = "".join(carries_int_syms)
    carry_frac_str = "".join(carries_frac_syms)

    op_a_display = f"{a_int_str}.{a_frac_str}" if has_frac else a_int_str
    op_b_display = f"{b_int_str}.{b_frac_str}" if has_frac else b_int_str
    carry_display = f"{carry_int_str} {carry_frac_str}" if has_frac else carry_int_str

    res_display = trace.result.to_string()
    width = max(
        len(op_a_display), len(op_b_display), len(res_display), len(carry_display), 8
    )

    lines = [
        f"--- CONTA ARMADA (ADIÇÃO NA BASE {base}) ---",
        f"  [vai-um]   {carry_display:>{width}}",
        f"             {op_a_display:>{width}}",
        f"        +    {op_b_display:>{width}}",
        f"        {'-' * (width + 5)}",
        f"             {res_display:>{width}}",
        "",
        "Passo a passo por coluna (da direita para a esquerda):",
    ]
    for step in trace.steps:
        lines.append(f"  • {step}")

    return "\n".join(lines)


def format_subtraction_conta_armada(trace: SubtractionTrace) -> str:
    """Formata visualmente a conta da subtração com alinhamento e linha de empréstimo."""
    base = trace.operand_a.base

    a_int_str = "".join(value_to_char(d, base) for d in trace.aligned_a_int)
    b_int_str = "".join(value_to_char(d, base) for d in trace.aligned_b_int)

    has_frac = len(trace.aligned_a_frac) > 0
    a_frac_str = (
        "".join(value_to_char(d, base) for d in trace.aligned_a_frac)
        if has_frac
        else ""
    )
    b_frac_str = (
        "".join(value_to_char(d, base) for d in trace.aligned_b_frac)
        if has_frac
        else ""
    )

    # Linha de empresta-um (borrows)
    borrows_int_syms = [
        str(b) if b > 0 else " "
        for b in trace.borrows_int[-len(trace.aligned_a_int) :]
    ]
    borrows_frac_syms = [str(b) if b > 0 else " " for b in trace.borrows_frac]

    borrow_int_str = "".join(borrows_int_syms)
    borrow_frac_str = "".join(borrows_frac_syms)

    op_a_display = f"{a_int_str}.{a_frac_str}" if has_frac else a_int_str
    op_b_display = f"{b_int_str}.{b_frac_str}" if has_frac else b_int_str
    borrow_display = f"{borrow_int_str} {borrow_frac_str}" if has_frac else borrow_int_str

    res_display = trace.result.to_string()
    width = max(
        len(op_a_display), len(op_b_display), len(res_display), len(borrow_display), 8
    )

    lines = [
        f"--- CONTA ARMADA (SUBTRAÇÃO NA BASE {base}) ---",
        f"  [empresta] {borrow_display:>{width}}",
        f"             {op_a_display:>{width}}",
        f"        -    {op_b_display:>{width}}",
        f"        {'-' * (width + 5)}",
        f"             {res_display:>{width}}",
        "",
        "Passo a passo por coluna (da direita para a esquerda):",
    ]
    for step in trace.steps:
        lines.append(f"  • {step}")

    return "\n".join(lines)


def format_conversion_report(res: ConversionResult) -> str:
    """Formata o relatório passo a passo da conversão direta entre bases."""
    lines = [
        "=" * 70,
        f"RELATÓRIO DE CONVERSÃO DIRETA DE BASE (SEM COERÇÃO DECIMAL)",
        "=" * 70,
        f"Número de Origem : {res.source_number.to_string()} (Base {res.source_number.base})",
        f"Base de Destino  : Base {res.target_base}",
        f"Resultado Final  : {res.result_number.to_string()} (Base {res.target_base})",
        "-" * 70,
        "[FASE 1] Conversão da Parte Inteira (Horner na Base de Destino):",
    ]
    for step in res.integer_steps:
        lines.append(f"  • {step}")

    lines.append("-" * 70)
    lines.append(
        f"[FASE 2] Conversão da Parte Fracionária (Multiplicações na Base de Origem):"
    )
    for step in res.fractional_steps:
        lines.append(f"  • {step}")

    lines.append("-" * 70)
    lines.append("[FASE 3] Diagnóstico de Periodicidade Fracionária:")
    if res.is_periodic:
        lines.append(f"  Status          : DÍZIMA PERIÓDICA IDENTIFICADA!")
        lines.append(
            f"  Início do ciclo : dígito {res.period_start + 1} após a vírgula"
        )
        lines.append(f"  Comprimento (T) : {res.period_length} dígitos")
        periodic_digits = res.result_number.fractional_digits[res.period_start :]
        p_str = "".join(
            value_to_char(d, res.target_base)
            for d in periodic_digits
        )
        lines.append(f"  Padrão repetido : ({p_str})")
    elif not res.source_number.fractional_digits:
        lines.append("  Status          : Número estritamente inteiro.")
    else:
        lines.append("  Status          : Fração exata finita (resto zerou).")

    lines.append("=" * 70)
    return "\n".join(lines)
