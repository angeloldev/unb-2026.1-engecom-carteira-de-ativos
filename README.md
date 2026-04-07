# 📈 Carteira de Investimentos — Engenharia Econômica

> Projeto desenvolvido para a disciplina de **Engenharia Econômica** da Faculdade de Ciências e Tecnologia em Engenharias (FCTE) — UnB 2026.1

Sistema Python completo para simulação, acompanhamento e análise de uma carteira de ativos financeiros de R$ 100.000,00, com coleta de dados reais via APIs, cálculos financeiros, análise de risco e geração automática de relatórios em PDF.

📚 **Documentação técnica completa das funções:** [`src/DOCUMENTACAO.md`](./src/DOCUMENTACAO.md)

---

## 🗂️ Estrutura do projeto

```
.
├── main.py                    # Ponto de entrada — orquestra todos os módulos
├── README.md                  # Este arquivo
├── requirements.txt           # Dependências do projeto
├── carteira.exemplo.json      # Modelo de carteira para novos usuários
├── .env                       # Variáveis de ambiente (não versionado)
├── .gitignore
│
└── src/                       # Pacote principal com toda a lógica
    ├── __init__.py            # Marca src/ como pacote Python
    ├── config.py              # Configurações centrais (capital, datas, URLs das APIs)
    ├── data_collector.py      # Coleta de dados via yfinance + API do Banco Central
    ├── portfolio_manager.py   # Cálculos financeiros (rentabilidade, resumo, benchmarks)
    ├── analytics.py           # Análise de risco (volatilidade, drawdown máximo)
    ├── report_generator.py    # Geração de relatório PDF com gráficos
    ├── csv_exporter.py        # Exportação de informe de rendimentos em CSV
    └── DOCUMENTACAO.md        # Documentação técnica de todas as funções
```

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.11+
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/angeloldev/unb-2026.1-engecom-carteira-de-ativos.git
cd unb-2026.1-engecom-carteira-de-ativos

# 2. Crie e ative o ambiente virtual
python3.11 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.exemplo .env
# Edite o .env com suas configurações

# 5. Configure a carteira
cp carteira.exemplo.json carteira.json
# Edite o carteira.json com seus ativos
```

---

## 🚀 Uso

```bash
python3 main.py
```

O sistema irá:
1. Coletar dados de todos os ativos via APIs
2. Calcular rentabilidade e métricas de risco
3. Comparar com benchmarks (SELIC e IPCA)
4. Gerar o relatório em `relatorio_carteira.pdf`
5. Exportar o informe de rendimentos em `rendimentos.csv`

---

## 📊 Ativos suportados

| Tipo | Exemplos | Fonte dos dados |
|---|---|---|
| Renda Fixa | CDB, Tesouro Selic, LCI, LCA | Simulação por juros compostos |
| Ações | PETR4.SA, VALE3.SA, ITUB4.SA | Yahoo Finance (yfinance) |
| ETFs | BOVA11.SA, IVVB11.SA | Yahoo Finance (yfinance) |
| FIIs | MXRF11.SA, HGLG11.SA | Yahoo Finance (yfinance) |
| Criptomoedas | BTC-USD, ETH-USD | Yahoo Finance (yfinance) |
| Benchmarks | SELIC, IPCA | API pública do Banco Central |

---

## 📁 Formato do `carteira.json`

```json
[
  {
    "nome": "Tesouro Selic 2027",
    "tipo": "Renda Fixa",
    "ticker": null,
    "valor_investido": 20000.00,
    "taxa_anual": 0.1275
  },
  {
    "nome": "Petrobras PN",
    "tipo": "Renda Variável",
    "ticker": "PETR4.SA",
    "valor_investido": 20000.00,
    "taxa_anual": null
  }
]
```

**Regras:**
- A soma de todos os `valor_investido` deve totalizar `CAPITAL_INICIAL` (padrão: R$ 100.000,00)
- Renda fixa: `ticker: null` e `taxa_anual` obrigatório
- Renda variável: `ticker` obrigatório e `taxa_anual: null`

---

## 🔑 Variáveis de ambiente (`.env`)

```dotenv
CAPITAL_INICIAL=100000.00
DATA_INICIO=2025-02-01
SELIC_URL=https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json
IPCA_URL=https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json
```

---

## 📦 Dependências principais

| Biblioteca | Versão | Finalidade |
|---|---|---|
| `yfinance` | ≥ 0.2 | Coleta de preços históricos de ações |
| `pandas` | ≥ 2.0 | Manipulação e análise de dados |
| `matplotlib` | ≥ 3.8 | Geração de gráficos |
| `reportlab` | ≥ 4.0 | Criação de relatórios em PDF |
| `requests` | ≥ 2.31 | Requisições HTTP para a API do BCB |
| `python-dotenv` | ≥ 1.0 | Carregamento de variáveis de ambiente |

---

## 📋 Relatórios gerados

O projeto cobre os requisitos das **3 entregas** da disciplina:

| Relatório | Conteúdo coberto |
|---|---|
| Relatório 1 | Composição da carteira, justificativa dos ativos, expectativa de retorno |
| Relatório 2 | Rentabilidade individual, comparação com SELIC e IPCA, análise crítica |
| Relatório 3 | Resultado final, análise de risco (volatilidade, drawdown), conclusão |

---

## 🏫 Informações acadêmicas

- **Aluno/Matrícula:** Ângelo Ararujo Cordova - 241025917
- **Disciplina:** Engenharia Econômica
- **Instituição:** Faculdade de Ciências e Tecnologia em Engenharias (FCTE) — UnB
- **Semestre:** 2026.1