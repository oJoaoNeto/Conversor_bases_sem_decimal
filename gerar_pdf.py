"""
Script para compilar o relatório Markdown em PDF acadêmico
com suporte completo a fórmulas matemáticas LaTeX (MathJax / KaTeX).
"""

import json
import os
import subprocess

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Relatório Técnico - Computação Numérica</title>
  <!-- KaTeX CSS e JS para renderização matemática ultra-rápida e síncrona -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
  <!-- Marked para Markdown -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    @page {
      size: A4;
      margin: 18mm 20mm;
    }
    body {
      font-family: 'Times New Roman', Times, serif, 'Segoe UI', sans-serif;
      font-size: 11.5pt;
      line-height: 1.6;
      color: #111;
      max-width: 820px;
      margin: 0 auto;
      padding: 20px;
      background: #fff;
    }
    h1, h2, h3, h4 {
      color: #0b2240;
      font-family: Arial, Helvetica, sans-serif;
      margin-top: 1.3em;
    }
    h1 {
      font-size: 16pt;
      text-align: center;
      border-bottom: 2px solid #0b2240;
      padding-bottom: 6px;
    }
    h2 {
      font-size: 13pt;
      border-bottom: 1px solid #ccc;
      padding-bottom: 4px;
    }
    h3 {
      font-size: 11.5pt;
    }
    pre, code {
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 9.5pt;
    }
    pre {
      background: #f8f9fa;
      border: 1px solid #dcdcdc;
      border-radius: 4px;
      padding: 10px 14px;
      overflow-x: auto;
      white-space: pre-wrap;
      line-height: 1.4;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 18px 0;
      font-size: 10.5pt;
    }
    th, td {
      border: 1px solid #888;
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background-color: #f1f3f5;
      font-weight: bold;
    }
    blockquote {
      border-left: 4px solid #0056b3;
      padding-left: 14px;
      margin-left: 0;
      color: #444;
      font-style: italic;
    }
    .katex {
      font-size: 1.08em;
    }
    .katex-display {
      margin: 0.8em 0;
    }
  </style>
</head>
<body>
  <div id="content"></div>
  <script>
    const markdownText = __MARKDOWN_RAW__;

    // Protege expressões LaTeX ($...$ e $$...$$) contra colisões do markdown
    const mathBlocks = [];
    let protectedText = markdownText.replace(/\$\$([\s\S]*?)\$\$/g, (match) => {
      mathBlocks.push(match);
      return `@@MATHBLOCK_${mathBlocks.length - 1}@@`;
    });
    protectedText = protectedText.replace(/\$([^\$\n]+?)\$/g, (match) => {
      mathBlocks.push(match);
      return `@@MATHINLINE_${mathBlocks.length - 1}@@`;
    });

    let htmlParsed = marked.parse(protectedText);

    // Restaura as fórmulas puras
    htmlParsed = htmlParsed.replace(/@@MATHBLOCK_(\d+)@@/g, (_, id) => mathBlocks[id]);
    htmlParsed = htmlParsed.replace(/@@MATHINLINE_(\d+)@@/g, (_, id) => mathBlocks[id]);

    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = htmlParsed;

    // Renderiza todas as fórmulas com KaTeX
    renderMathInElement(contentDiv, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false}
      ],
      throwOnError: false
    });
  </script>
</body>
</html>"""

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(base_dir, "relatorio.md")
    html_path = os.path.join(base_dir, "relatorio.html")
    pdf_path = os.path.join(base_dir, "relatorio.pdf")

    if not os.path.exists(md_path):
        print(f"Erro: Arquivo {md_path} não encontrado.")
        return

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    json_content = json.dumps(md_text)
    html_content = HTML_TEMPLATE.replace("__MARKDOWN_RAW__", json_content)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] HTML gerado em: {html_path}")

    # Tenta usar o Chrome headless para gerar o PDF automaticamente
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    chrome_cmd = None
    for p in chrome_paths:
        if os.path.exists(p):
            chrome_cmd = p
            break

    if chrome_cmd:
        print("[INFO] Gerando PDF acadêmico com Google Chrome...")
        cmd = [
            chrome_cmd,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=6000",
            f"--print-to-pdf={pdf_path}",
            f"file:///{html_path.replace(os.sep, '/')}"
        ]
        try:
            subprocess.run(cmd, check=True)
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"[SUCESSO] PDF gerado em: {pdf_path} ({file_size} bytes)")
                return
        except Exception as e:
            print(f"[AVISO] Falha na exportação automática: {e}")

    print("[INFO] Você pode abrir 'relatorio.html' no seu navegador e pressionar Ctrl+P -> Salvar como PDF.")

if __name__ == "__main__":
    main()
