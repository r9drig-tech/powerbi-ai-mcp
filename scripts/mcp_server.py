"""
PowerBI AI MCP Server
=====================
Servidor MCP que expõe ferramentas para geração, explicação e organização
de medidas DAX via linguagem natural, usando Claude como motor de IA.

Autor  : Rodrigo Salgado | github.com/r9drig-tech
Projeto: powerbi-ai-mcp
"""

import json
import re
from anthropic import Anthropic

# ── Inicialização ────────────────────────────────────────────────────────────
client = Anthropic()

SYSTEM_PROMPT = """Você é um especialista em Power BI e DAX com foco em produtividade.
Suas respostas são sempre diretas, técnicas e prontas para uso imediato.

Ao gerar medidas DAX:
- Use formatação limpa e consistente
- Adicione comentários inline quando a lógica for complexa
- Siga as boas práticas de nomenclatura (sem espaços, PascalCase)
- Sempre considere tratamento de divisão por zero com DIVIDE()
- Use CALCULATE, FILTER, ALL conforme necessário

Ao explicar medidas:
- Descreva o que calcula, como funciona e onde usar
- Mencione possíveis variações ou alternativas

Ao sugerir KPIs:
- Agrupe por área de análise (Financeiro, Operacional, Comercial)
- Indique prioridade (P1 = crítico, P2 = importante, P3 = complementar)

Responda sempre em português brasileiro."""

TOOLS = {
    "create_measure": {
        "description": "Gera uma medida DAX a partir de linguagem natural",
        "handler": "_create_measure"
    },
    "explain_measure": {
        "description": "Explica o que uma medida DAX faz",
        "handler": "_explain_measure"
    },
    "suggest_kpis": {
        "description": "Sugere KPIs para um domínio de negócio",
        "handler": "_suggest_kpis"
    },
    "create_calendar": {
        "description": "Gera código DAX para tabela Calendário",
        "handler": "_create_calendar"
    },
    "organize_measures": {
        "description": "Sugere estrutura de pastas para organizar medidas",
        "handler": "_organize_measures"
    },
    "document_model": {
        "description": "Documenta todas as medidas de um modelo",
        "handler": "_document_model"
    },
}


# ── Handlers ─────────────────────────────────────────────────────────────────

def _create_measure(user_input: str) -> str:
    """Gera medida DAX a partir de uma descrição em linguagem natural."""
    prompt = f"""Crie uma medida DAX para Power BI com base nesta solicitação:

"{user_input}"

Formato de resposta:
1. Nome sugerido para a medida
2. Código DAX completo (bloco de código)
3. Uma linha explicando o que a medida calcula
4. Sugestão de pasta/display folder

Responda de forma concisa e objetiva."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def _explain_measure(dax_code: str) -> str:
    """Explica uma medida DAX existente."""
    prompt = f"""Explique esta medida DAX de forma clara e didática:

```dax
{dax_code}
```

Estruture a explicação em:
- O que calcula
- Como funciona (passo a passo da lógica)
- Contexto de uso recomendado
- Possíveis armadilhas ou pontos de atenção"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def _suggest_kpis(domain: str) -> str:
    """Sugere KPIs para um domínio de negócio."""
    prompt = f"""Sugira os principais KPIs para um dashboard de {domain}.

Para cada KPI, forneça:
- Nome do KPI
- Prioridade (P1/P2/P3)
- Fórmula DAX básica
- Categoria (Financeiro / Operacional / Comercial / Qualidade)

Organize do mais crítico para o complementar. Máximo 10 KPIs."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def _create_calendar() -> str:
    """Gera tabela Calendário em DAX."""
    prompt = """Gere o código DAX completo para criar uma tabela Calendário (dCalendario) 
no Power BI com as seguintes colunas:
- Data, Ano, Mes (número), NomeMes, MesAbrev, Trimestre, NomeTrimestre,
  Semana, DiaSemana, NomeDiaSemana, AnoMes (YYYYMM), AnoTrimestre,
  IsDiaSemana (boolean), IsFinaneiro (boolean para anos fiscais)

Use CALENDARAUTO() como base e ADDCOLUMNS para adicionar as colunas.
Inclua configuração de sort para NomeMes e NomeDiaSemana.
Comente cada coluna calculada."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def _organize_measures(measures_list: str) -> str:
    """Sugere estrutura de pastas para organizar medidas."""
    prompt = f"""Organize as seguintes medidas em pastas (display folders) para Power BI:

{measures_list}

Crie uma estrutura lógica de pastas no padrão:
📁 NomePasta
  └─ MedidaA
  └─ MedidaB

Use emojis para tornar visual. Explique brevemente o critério de agrupamento."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def _document_model(measures_json: str) -> str:
    """Documenta todas as medidas de um modelo Power BI."""
    prompt = f"""Gere uma documentação técnica completa para as seguintes medidas do modelo Power BI:

{measures_json}

Formato de saída (Markdown):
## Documentação do Modelo — [Data Atual]

### Resumo
- Total de medidas: X
- Pastas: Y

### Medidas por Pasta

#### [Nome da Pasta]
| Medida | Descrição | Fórmula | Dependências |
|--------|-----------|---------|--------------|
| ...    | ...       | ...     | ...          |

Seja técnico e objetivo."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


# ── Interface CLI (modo conversacional) ──────────────────────────────────────

def run_cli():
    """Modo interativo via terminal — simula o uso do MCP no Claude Desktop."""
    print("\n" + "="*60)
    print("  PowerBI AI MCP Server — Modo Interativo")
    print("  github.com/r9drig-tech/powerbi-ai-mcp")
    print("="*60)
    print("\nFerramentas disponíveis:")
    for name, info in TOOLS.items():
        print(f"  • {name}: {info['description']}")
    print("\nExemplos de uso:")
    print("  > Crie uma medida de Receita Total")
    print("  > Explique: [cole o código DAX aqui]")
    print("  > Sugira KPIs para vendas")
    print("  > Crie tabela calendário")
    print("  > Organize: Receita Total, Lucro, Margem %, Ticket Médio")
    print("\nDigite 'sair' para encerrar.\n")

    conversation = []

    while True:
        try:
            user_input = input("você > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando servidor MCP.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("sair", "exit", "quit"):
            print("Até logo!")
            break

        conversation.append({"role": "user", "content": user_input})

        # Roteamento simples por palavra-chave
        lower = user_input.lower()
        result = None

        if any(k in lower for k in ["crie", "criar", "gere", "gerar", "medida", "measure"]):
            if "calendário" in lower or "calendario" in lower or "calendar" in lower:
                result = _create_calendar()
            else:
                result = _create_measure(user_input)
        elif any(k in lower for k in ["explique", "explicar", "explica", "o que faz", "what"]):
            # Extrai código DAX se estiver presente
            dax_match = re.search(r"```[\s\S]*?```|(?:explique[:\s]+)([\s\S]+)", user_input, re.IGNORECASE)
            dax_code = dax_match.group(0) if dax_match else user_input
            result = _explain_measure(dax_code)
        elif any(k in lower for k in ["kpi", "indicador", "sugira", "sugerir", "sugere"]):
            result = _suggest_kpis(user_input)
        elif any(k in lower for k in ["organize", "organizar", "pasta", "folder"]):
            result = _organize_measures(user_input)
        elif any(k in lower for k in ["document", "documenta", "documentar"]):
            result = _document_model(user_input)
        else:
            # Fallback: envia direto ao Claude com contexto Power BI
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=800,
                system=SYSTEM_PROMPT,
                messages=conversation
            )
            result = response.content[0].text

        print(f"\nIA  > {result}\n")
        conversation.append({"role": "assistant", "content": result})


# ── Entrypoint ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_cli()
