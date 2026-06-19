# 🤖 Power BI + AI + MCP — Controlando o Power BI com Inteligência Artificial

<div align="center">

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude%20AI-D97757?style=for-the-badge&logo=anthropic&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-6366f1?style=for-the-badge)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)

**Criação de medidas DAX, explicação de métricas, sugestão de KPIs e organização do modelo — tudo via linguagem natural.**

[🚀 Começar](#instalação) · [📊 Ver Dashboard](#dashboard) · [📝 Medidas DAX](#medidas-geradas)

</div>

---

## 🎯 O que este projeto faz

Este projeto demonstra como o **Model Context Protocol (MCP)** conecta o **Claude AI** diretamente ao fluxo de trabalho do Power BI, permitindo que você:

| Comando em linguagem natural | O que a IA faz |
|---|---|
| *"Crie uma medida de Receita Total"* | Gera o DAX completo e pronto para uso |
| *"Explique todas as medidas do modelo"* | Documenta cada medida com descrição técnica |
| *"Sugira KPIs para um dashboard executivo"* | Lista KPIs priorizados por área de negócio |
| *"Organize as medidas em pastas"* | Propõe estrutura de display folders |
| *"Crie uma tabela calendário"* | Gera dCalendario completa em DAX |
| *"Documente o projeto"* | Gera documentação Markdown do modelo |

---

## 🏗️ Arquitetura

```
Claude Desktop / Terminal
        │
        ▼
   MCP Server (Python)
        │
        ├── Tool: create_measure()    ──► Claude API ──► DAX gerado
        ├── Tool: explain_measure()   ──► Claude API ──► Documentação
        ├── Tool: suggest_kpis()      ──► Claude API ──► Lista de KPIs
        ├── Tool: create_calendar()   ──► Claude API ──► dCalendario DAX
        ├── Tool: organize_measures() ──► Claude API ──► Estrutura de pastas
        └── Tool: document_model()    ──► Claude API ──► README do modelo
                                              │
                                     Resultado colado no
                                     Power BI Desktop
```

---

## 📁 Estrutura do Projeto

```
powerbi-ai-mcp/
│
├── data/
│   └── vendas.csv              # Dataset de vendas (60 registros, 6 meses)
│
├── scripts/
│   ├── mcp_server.py           # Servidor MCP com todas as ferramentas de IA
│   ├── medidas_dax.dax         # Medidas geradas pela IA (25+ medidas)
│   └── dCalendario.dax         # Tabela Calendário PT-BR completa
│
├── docs/
│   └── arquitetura.png         # Diagrama da solução
│
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

O arquivo `data/vendas.csv` contém **60 registros** simulando 6 meses de vendas de uma loja de tecnologia:

| Coluna | Descrição |
|---|---|
| `Data` | Data da venda |
| `Produto` | Nome do produto |
| `Categoria` | Eletrônicos, Periféricos, Monitores, Armazenamento, Mobiliário |
| `Regiao` | Sul, Norte, Sudeste, Centro-Oeste, Nordeste |
| `Vendedor` | 5 vendedores distintos |
| `Qtd` | Quantidade vendida |
| `Valor_Unitario` | Preço de venda unitário |
| `Custo_Unitario` | Custo unitário do produto |
| `Valor_Venda` | Receita total da linha |
| `Custo_Total` | Custo total da linha |

---

## 📐 Medidas Geradas

A IA gerou **25+ medidas DAX** organizadas em 6 pastas:

### 💰 Financeiro
```dax
Receita Total = SUM(Vendas[Valor_Venda])

Lucro = [Receita Total] - [Custo Total]

Margem % = DIVIDE([Lucro], [Receita Total], 0)

Ticket Médio = DIVIDE([Receita Total], [Total Pedidos], 0)
```

### 📈 Crescimento
```dax
Crescimento MoM % =
DIVIDE(
    [Receita Total] - [Receita MêsAnterior],
    [Receita MêsAnterior],
    0
)

Crescimento YoY % =
DIVIDE(
    [Receita Total] - [Receita MesmoPeríodo AA],
    [Receita MesmoPeríodo AA],
    0
)
```

### 🏆 Ranking
```dax
Rank Produto Receita =
RANKX(ALL(Vendas[Produto]), [Receita Total],, DESC, DENSE)
```

> 📄 Ver arquivo completo: [`scripts/medidas_dax.dax`](scripts/medidas_dax.dax)

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.11+
- Chave de API da Anthropic: [console.anthropic.com](https://console.anthropic.com)
- Power BI Desktop (para usar os arquivos DAX)

### Setup

```bash
# Clone o repositório
git clone https://github.com/r9drig-tech/powerbi-ai-mcp
cd powerbi-ai-mcp

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure sua chave de API
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Executar o servidor MCP

```bash
python scripts/mcp_server.py
```

**Exemplo de sessão:**

```
você > Crie uma medida de Receita Total usando a coluna Valor_Venda

IA  > **Receita Total**

    ```dax
    Receita Total =
    SUM(Vendas[Valor_Venda])
    ```

    Soma todos os valores da coluna Valor_Venda da tabela Vendas.
    Pasta sugerida: 💰 Financeiro

você > Crie uma medida de Margem de Lucro em percentual

IA  > **Margem %**

    ```dax
    Margem % =
    DIVIDE(
        [Lucro],
        [Receita Total],
        0
    )
    ```

    Calcula a margem de lucro como proporção da receita.
    Usa DIVIDE() para evitar erro de divisão por zero.
    Pasta sugerida: 💰 Financeiro

você > Sugira KPIs para um dashboard executivo de vendas

IA  > **KPIs para Dashboard Executivo — Vendas**

    🔴 P1 — Críticos
    • Receita Total | SUM(Vendas[Valor_Venda])
    • Margem % | DIVIDE([Lucro],[Receita Total])
    • Crescimento MoM % | variação vs mês anterior

    🟡 P2 — Importantes
    • Ticket Médio | Receita / Nº de pedidos
    • Top 10 Produtos | RANKX por receita
    • Receita por Região | segmentação geográfica

    🟢 P3 — Complementares
    • Receita Acumulada no Ano (YTD)
    • Crescimento YoY %
    • Taxa de Retorno de Clientes
```

---

## 🎬 Demo

> Claude Desktop à esquerda + Power BI à direita.
> Prompts em linguagem natural → medidas DAX prontas em segundos.

**→ [Abrir demo interativo](docs/demo_screens.html)**

| Cena | Prompt | Resultado |
|------|--------|-----------|
| 1 | `Crie uma medida de Receita Total` | DAX gerado + pasta sugerida |
| 2 | `Crie Margem de Lucro em percentual` | DIVIDE() com fallback |
| 3 | `Sugira KPIs para dashboard executivo` | 8 KPIs priorizados P1/P2/P3 |
| 4 | `Organize as medidas em pastas` | 6 display folders automáticas |
| 5 | Dashboard pronto | 6 KPIs + Top 5 produtos |

---

## 🛠️ Stack Tecnológica

| Ferramenta | Uso |
|---|---|
| **Power BI Desktop** | Modelagem e visualização |
| **Claude AI (Anthropic)** | Geração e explicação de DAX |
| **MCP (Model Context Protocol)** | Protocolo de comunicação IA ↔ ferramentas |
| **Python 3.11+** | Servidor MCP |
| **VS Code** | Edição e desenvolvimento |
| **OBS Studio** | Gravação do vídeo demo |

---

## 📌 Roadmap

- [x] Dataset de vendas estruturado
- [x] Servidor MCP com 6 ferramentas
- [x] 25+ medidas DAX geradas por IA
- [x] Tabela Calendário PT-BR completa
- [ ] Dashboard .pbix exportado
- [ ] Integração via Claude Desktop (config MCP)
- [ ] Vídeo demo no YouTube/LinkedIn
- [ ] Diagrama de arquitetura visual

---

## 👤 Autor

**Rodrigo Salgado**
Analista de BI & Dados | Em transição para Engenharia de Dados & IA

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/rodrigo-salgado-bi)


---

## 📄 Licença

MIT License — use, adapte e compartilhe com os devidos créditos.
