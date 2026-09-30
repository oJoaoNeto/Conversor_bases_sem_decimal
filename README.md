# Conversão de Bases e Operações Elementares Sem Coerção Decimal

**ECT-3401: Computação Numérica — Projeto da Unidade I**  
**Universidade Federal do Rio Grande do Norte (UFRN)**  
**Docente:** Prof. Dr. Joilson B. A. Rego  

---

## 📌 Visão Geral

Este projeto implementa um ambiente computacional em **Python 3.11+** voltado à aritmética de sistemas posicionais arbitrários ($2 \le \text{Base} \le 36$), atendendo a três metas fundamentais:
1. **Operações Elementares (Adição e Subtração):** Implementadas diretamente na base selecionada, calculadas coluna a coluna através de vetores de dígitos e renderizadas visualmente no terminal como **contas armadas**, com rastreio explícito de *vai-um* (*carry*) e *empresta-um* (*borrow*).
2. **Conversão Direta de Base sem Coerção Decimal:** Conversão de números reais ($x \in \mathbb{R}$) calculada estritamente na base de origem ou de destino, **sem utilizar tipos primitivos `float` (IEEE 754) ou a base decimal (10) como pivô intermediário**.
   - **Parte Inteira:** Avaliada na base de destino via **Algoritmo de Horner** utilizando a própria adição da base de destino.
   - **Parte Fracionária:** Avaliada na base de origem via **multiplicações sucessivas** pela base de destino utilizando a própria adição da base de origem.
3. **Detecção Exata de Dízimas Periódicas Nativas:** Rastreamento do histórico de estados fracionários na base de origem, permitindo identificar o período exato (início e comprimento do ciclo repetitivo) diretamente na base de destino sem ruídos de truncamento de hardware.

---

## 📂 Estrutura de Diretórios

```text
projeto_u1/
├── README.md               # Este documento explicativo
├── relatorio.md            # Relatório acadêmico completo com análise crítica e resultados
├── requirements.txt        # Dependências opcionais (ex: pytest)
├── main.py                 # Interface CLI interativa (Menu principal)
├── src/
│   ├── __init__.py
│   ├── alphabet.py         # Mapeamento dinâmico de símbolos/dígitos (0-9, A-Z)
│   ├── base_number.py      # Estrutura vetorial de dígitos isolados (BaseNumber)
│   ├── operations.py       # Algoritmos de Adição e Subtração com geração de traces
│   ├── converter.py        # Conversor direto sem coerção decimal e detecção de dízimas
│   └── display.py          # Renderização de contas armadas e relatórios passo a passo
└── tests/
    ├── __init__.py
    ├── test_operations.py   # Testes unitários para adição, subtração, carries e borrows
    ├── test_converter.py    # Testes unitários para conversão direta entre bases não-decimais
    └── test_dizimas.py      # Testes unitários de detecção exata de dízimas periódicas nativas
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
- Python 3.11 ou superior instalado.
- Nenhuma biblioteca externa é obrigatória para a execução do programa principal.

### 2. Executando o Menu Interativo (CLI)
No terminal, a partir da pasta `projeto_u1`:
```bash
python main.py
```
O menu interativo oferece:
1. **Operações Elementares (Adição e Subtração):** Escolha qualquer base (2 a 36) e dois operandos reais para visualizar a conta armada e a resolução coluna a coluna.
2. **Conversão Direta de Bases:** Converta números reais entre quaisquer bases arbitrárias (ex: Base 4 para Base 3, Base 7 para Base 13, Base 10 para Binário) acompanhando o passo a passo da aritmética polinomial e o diagnóstico de periodicidade.
3. **Demonstrações e Casos Didáticos:** Executa automaticamente 4 casos clássicos ilustrativos.
4. **Executar Bateria de Testes:** Executa todos os testes automatizados diretamente pela aplicação.

### 3. Executando os Testes Automatizados
Via módulo nativo `unittest`:
```bash
python -m unittest discover tests
```
Ou via `pytest` (caso instalado):
```bash
pytest tests/ -v
```

---

## 🔬 Fundamentação Algorítmica

### Eliminação da Coerção Decimal
O uso de tipos primitivos `float` (padrão IEEE 754) para intermediar conversões de base introduz erros de representação (como $0.1_{10}$ tornando-se uma dízima em binário), confundindo números finitos com periódicos. A nossa solução trata os números como a classe `BaseNumber`, que armazena vetores de inteiros puros para a parte inteira e a fracionária.

- **Inteiro via Horner na Base Destino ($B_2$):**
  $$P_k = P_{k+1} \times B_1 + d_k$$
  O produto $P \times B_1$ é calculado através de adições sucessivas (ou *double-and-add*) executadas na base $B_2$.
- **Fracionário via Multiplicações Sucessivas na Base Origem ($B_1$):**
  $$F_{k} = (F_{k-1} \times B_2) \pmod 1, \quad d = \lfloor F_{k-1} \times B_2 \rfloor$$
  As multiplicações são executadas na base $B_1$. Ao salvar os estados intermediários de $F_k$ como tuplas exatas de dígitos inteiros, a igualdade $F_k = F_j$ identifica a periodicidade sem qualquer margem de tolerância ($\epsilon$), assegurando precisão analítica.

---

## 📄 Relatório Técnico
O relatório acadêmico completo exigido para a avaliação (item 3 dos resultados esperados) encontra-se redigido no arquivo [`relatorio.md`](file:///C:/Users/JoaoNeto/Documents/ufrn/CN/projeto_u1/relatorio.md).
# Conversor_bases_sem_decimal
