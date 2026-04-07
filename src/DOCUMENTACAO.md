# 📚 Documentação Técnica — Carteira de Investimentos

> Referência completa de todas as funções do projeto, organizada por módulo.

---

## `config.py`

Módulo de configurações centrais. Não contém funções — define constantes e carrega dados.

### Constantes exportadas

| Constante | Tipo | Descrição |
|---|---|---|
| `CAPITAL_INICIAL` | `float` | Valor total a ser investido. Carregado do `.env`. |
| `DATA_INICIO` | `str` | Data de início da carteira no formato ISO 8601 (`"YYYY-MM-DD"`). |
| `BENCHMARKS` | `dict` | Dicionário com URLs da API do Banco Central para SELIC e IPCA. |
| `CARTEIRA` | `list[dict]` | Lista de ativos carregada do `carteira.json`. |

### Exemplo de uso

```python
from config import CARTEIRA, CAPITAL_INICIAL, DATA_INICIO, BENCHMARKS

print(CAPITAL_INICIAL)        # 100000.0
print(DATA_INICIO)            # "2025-02-01"
print(CARTEIRA[0]["nome"])    # "Tesouro Selic 2027"
```

---

## `data_collector.py`

Responsável por coletar dados de todas as fontes externas e internas.

---

### `buscar_renda_variavel(ativo, data_inicio)`

Busca o histórico de preços de um ativo de renda variável via Yahoo Finance e calcula o valor proporcional ao capital investido.

**Parâmetros:**
- `ativo` (`dict`) — dicionário do ativo conforme estrutura do `carteira.json`
- `data_inicio` (`str`) — data de início no formato `"YYYY-MM-DD"`

**Retorna:** `pd.DataFrame` com as colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `Date` | `datetime` | Data do pregão |
| `nome` | `str` | Nome do ativo |
| `tipo` | `str` | Tipo do ativo (ex: "Renda Variável") |
| `valor_inicial` | `float` | Valor investido originalmente |
| `valor_atual` | `float` | Valor da posição naquele dia |

Retorna `pd.DataFrame()` vazio em caso de erro.

**Exemplo:**
```python
ativo = {"nome": "Petrobras PN", "tipo": "Renda Variável", "ticker": "PETR4.SA", "valor_investido": 20000.0}
df = buscar_renda_variavel(ativo, "2025-02-01")
```

---

### `simular_renda_fixa(ativo, data_inicio)`

Simula o crescimento diário de um ativo de renda fixa usando juros compostos. Utiliza a convenção de 252 dias úteis por ano do mercado financeiro brasileiro.

**Fórmula aplicada:**
```
taxa_diaria = (1 + taxa_anual)^(1/252) - 1
valor_dia_N = valor_investido × (1 + taxa_diaria)^N
```

**Parâmetros:**
- `ativo` (`dict`) — dicionário do ativo com `taxa_anual` definida
- `data_inicio` (`str`) — data de início no formato `"YYYY-MM-DD"`

**Retorna:** `pd.DataFrame` com as mesmas colunas de `buscar_renda_variavel`, uma linha por dia corrido desde `data_inicio` até hoje.

**Exemplo:**
```python
ativo = {"nome": "CDB Banco XP", "tipo": "Renda Fixa", "ticker": None, "valor_investido": 15000.0, "taxa_anual": 0.13}
df = simular_renda_fixa(ativo, "2025-02-01")
```

---

### `buscar_benchmarks(data_inicio)`

Busca as taxas diárias da SELIC e do IPCA na API pública do Banco Central do Brasil. Não requer autenticação.

**Parâmetros:**
- `data_inicio` (`str` ou `datetime`) — data de início da consulta

**Retorna:** `dict` onde cada chave é o nome do benchmark (`"selic"`, `"ipca"`) e o valor é um `pd.DataFrame` com as colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `data` | `datetime` | Data da taxa |
| `valor` | `float` | Taxa diária naquele dia |

**Exemplo:**
```python
benchmarks = buscar_benchmarks("2025-02-01")
print(benchmarks["selic"].head())
```

---

### `coletar_dados()`

Função principal do módulo. Orquestra as três fontes de dados e retorna tudo unificado.

**Parâmetros:** nenhum — usa `CARTEIRA`, `DATA_INICIO` e `BENCHMARKS` do `config.py`.

**Retorna:** tupla `(df_carteira, df_benchmarks)`
- `df_carteira` (`pd.DataFrame`) — todos os ativos, todas as datas, formato unificado
- `df_benchmarks` (`dict`) — dicionário com DataFrames de SELIC e IPCA

**Exemplo:**
```python
df_carteira, df_benchmarks = coletar_dados()
print(df_carteira["nome"].unique())   # todos os ativos coletados
```

---

## `portfolio_manager.py`

Responsável por todos os cálculos financeiros sobre os dados coletados.

---

### `calcular_rentabilidade(df_carteira)`

Calcula a rentabilidade individual de cada ativo com base no último dia disponível.

**Fórmula:**
```
rentabilidade_pct = ((valor_atual - valor_inicial) / valor_inicial) × 100
ganho_reais = valor_atual - valor_inicial
```

**Parâmetros:**
- `df_carteira` (`pd.DataFrame`) — DataFrame retornado por `coletar_dados()`

**Retorna:** `pd.DataFrame` com as colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `nome` | `str` | Nome do ativo |
| `tipo` | `str` | Tipo do ativo |
| `valor_inicial` | `float` | Valor investido originalmente |
| `valor_atual` | `float` | Valor atual da posição |
| `ganho_reais` | `float` | Lucro ou prejuízo em R$ |
| `rentabilidade_pct` | `float` | Rentabilidade acumulada em % |

**Exemplo:**
```python
df_rent = calcular_rentabilidade(df_carteira)
print(df_rent[["nome", "rentabilidade_pct"]])
```

---

### `calcular_resumo_carteira(df_rentabilidade)`

Agrega os dados individuais e calcula a performance da carteira inteira.

**Parâmetros:**
- `df_rentabilidade` (`pd.DataFrame`) — retorno de `calcular_rentabilidade()`

**Retorna:** tupla `(resumo, df_rentabilidade)`
- `resumo` (`dict`) — dicionário com as chaves: `capital_inicial`, `valor_atual`, `ganho_reais`, `rentabilidade_pct`
- `df_rentabilidade` — o mesmo DataFrame recebido, retornado para encadeamento

**Exemplo:**
```python
resumo, _ = calcular_resumo_carteira(df_rent)
print(f"Rentabilidade total: {resumo['rentabilidade_pct']:.2f}%")
```

---

### `comparar_benchmarks(df_carteira, df_benchmarks)`

Compara a rentabilidade da carteira com os benchmarks SELIC e IPCA no mesmo período.

**Parâmetros:**
- `df_carteira` (`pd.DataFrame`) — DataFrame retornado por `coletar_dados()`
- `df_benchmarks` (`dict`) — dicionário retornado por `coletar_dados()`

**Retorna:** `dict` com a rentabilidade acumulada de cada indicador:
```python
{"Carteira": 30.23, "SELIC": 15.85, "IPCA": 5.06}
```

**Exemplo:**
```python
comparacao = comparar_benchmarks(df_carteira, df_benchmarks)
for nome, valor in comparacao.items():
    print(f"{nome}: {valor:.2f}%")
```

---

## `analytics.py`

Responsável pelas métricas de risco da carteira.

---

### `calcular_volatilidade(df_carteira)`

Calcula a volatilidade de cada ativo como o desvio padrão dos retornos diários percentuais.

Alta volatilidade = ativo oscila muito = maior risco. Baixa volatilidade = crescimento estável.

**Parâmetros:**
- `df_carteira` (`pd.DataFrame`) — DataFrame retornado por `coletar_dados()`

**Retorna:** `pd.DataFrame` com as colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `nome` | `str` | Nome do ativo |
| `volatilidade_pct` | `float` | Desvio padrão dos retornos diários em % |

**Exemplo:**
```python
df_vol = calcular_volatilidade(df_carteira)
# Bitcoin: ~2.4%  |  Tesouro Selic: ~0.0%
```

---

### `calcular_drawdown(df_carteira)`

Calcula o drawdown máximo de cada ativo — a maior queda percentual em relação ao pico histórico.

**Fórmula:**
```
drawdown_dia = (valor_atual - pico_acumulado) / pico_acumulado × 100
max_drawdown = mínimo de todos os drawdowns diários
```

**Parâmetros:**
- `df_carteira` (`pd.DataFrame`) — DataFrame retornado por `coletar_dados()`

**Retorna:** `pd.DataFrame` com as colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `nome` | `str` | Nome do ativo |
| `max_drawdown_pct` | `float` | Maior queda em relação ao pico histórico (valor negativo) |

**Exemplo:**
```python
df_dd = calcular_drawdown(df_carteira)
# Bitcoin: -49.74%  |  CDB: 0.0%
```

---

### `resumo_risco(df_carteira)`

Combina volatilidade e drawdown em uma única tabela de análise de risco.

**Parâmetros:**
- `df_carteira` (`pd.DataFrame`) — DataFrame retornado por `coletar_dados()`

**Retorna:** `pd.DataFrame` com as colunas `nome`, `volatilidade_pct` e `max_drawdown_pct`.

**Exemplo:**
```python
df_risco = resumo_risco(df_carteira)
print(df_risco.to_string(index=False))
```

---

## `report_generator.py`

Responsável pela geração visual do relatório em PDF.

---

### `gerar_grafico_pizza(df_rentabilidade, caminho)`

Gera gráfico de pizza com a composição percentual da carteira por valor investido.

**Parâmetros:**
- `df_rentabilidade` (`pd.DataFrame`) — retorno de `calcular_rentabilidade()`
- `caminho` (`str`) — caminho onde salvar a imagem `.png`

---

### `gerar_grafico_rentabilidade(df_rentabilidade, caminho)`

Gera gráfico de barras horizontais com a rentabilidade de cada ativo. Barras verdes para ganho, vermelhas para perda.

**Parâmetros:**
- `df_rentabilidade` (`pd.DataFrame`) — retorno de `calcular_rentabilidade()`
- `caminho` (`str`) — caminho onde salvar a imagem `.png`

---

### `gerar_grafico_evolucao(df_carteira, caminho)`

Gera gráfico de linha com a evolução do valor total da carteira ao longo do tempo. Inclui linha tracejada indicando o capital inicial.

**Parâmetros:**
- `df_carteira` (`pd.DataFrame`) — DataFrame retornado por `coletar_dados()`
- `caminho` (`str`) — caminho onde salvar a imagem `.png`

---

### `gerar_grafico_benchmark(comparacao, caminho)`

Gera gráfico de barras comparando a rentabilidade da carteira com SELIC e IPCA.

**Parâmetros:**
- `comparacao` (`dict`) — retorno de `comparar_benchmarks()`
- `caminho` (`str`) — caminho onde salvar a imagem `.png`

---

### `gerar_relatorio_pdf(df_carteira, df_rentabilidade, resumo, comparacao, df_risco, caminho_pdf)`

Função principal do módulo. Orquestra a geração de todos os gráficos e monta o PDF completo.

**Parâmetros:**
- `df_carteira` (`pd.DataFrame`) — retorno de `coletar_dados()`
- `df_rentabilidade` (`pd.DataFrame`) — retorno de `calcular_rentabilidade()`
- `resumo` (`dict`) — retorno de `calcular_resumo_carteira()`
- `comparacao` (`dict`) — retorno de `comparar_benchmarks()`
- `df_risco` (`pd.DataFrame`) — retorno de `resumo_risco()`
- `caminho_pdf` (`str`, opcional) — caminho do arquivo gerado. Padrão: `"relatorio.pdf"`

**Efeitos:**
- Cria a pasta `graficos/` se não existir
- Salva 4 imagens `.png` em `graficos/`
- Gera o arquivo PDF no caminho especificado

**Exemplo:**
```python
gerar_relatorio_pdf(
    df_carteira=df_carteira,
    df_rentabilidade=df_rent,
    resumo=resumo,
    comparacao=comparacao,
    df_risco=resumo_risco(df_carteira),
    caminho_pdf="relatorio_carteira.pdf"
)
```

---

## `csv_exporter.py`

Responsável pela exportação do informe de rendimentos.

---

### `exportar_informe(df_rentabilidade, resumo, caminho_csv)`

Exporta um informe de rendimentos completo em formato CSV.

**Parâmetros:**
- `df_rentabilidade` (`pd.DataFrame`) — retorno de `calcular_rentabilidade()`
- `resumo` (`dict`) — retorno de `calcular_resumo_carteira()`
- `caminho_csv` (`str`, opcional) — caminho do arquivo gerado. Padrão: `"rendimentos.csv"`

**Arquivo gerado:**

| Coluna | Descrição |
|---|---|
| `Ativo` | Nome do ativo |
| `Tipo` | Renda Fixa / Renda Variável / Outros |
| `Valor Investido (R$)` | Capital alocado no ativo |
| `Valor Atual (R$)` | Posição atual |
| `Ganho (R$)` | Lucro ou prejuízo em reais |
| `Rentabilidade (%)` | Rentabilidade acumulada |

---

## `main.py`

Ponto de entrada do sistema. Orquestra todos os módulos em sequência.

### Fluxo de execução

```
1. coletar_dados()              → busca todos os dados
2. calcular_rentabilidade()     → calcula performance por ativo
3. calcular_resumo_carteira()   → agrega visão geral
4. comparar_benchmarks()        → compara com CDI e IPCA
5. resumo_risco()               → calcula volatilidade e drawdown
6. gerar_relatorio_pdf()        → gera relatorio_carteira.pdf
7. exportar_informe()           → gera rendimentos.csv
```

---

## 🗺️ Diagrama de dependências

```
main.py
├── data_collector.py
│   └── config.py
├── portfolio_manager.py
├── analytics.py
├── report_generator.py
└── csv_exporter.py
```

---

## 🔮 Roadmap — funcionalidades futuras

- [ ] Interface visual com **Streamlit** para adicionar/remover ativos sem editar JSON
- [ ] Suporte a **rebalanceamento** da carteira com registro histórico de movimentações
- [ ] Cálculo de **correlação entre ativos** para análise de diversificação
- [ ] Otimização de portfólio com **teoria de Markowitz**
- [ ] Exportação do relatório em formato **Word (.docx)**