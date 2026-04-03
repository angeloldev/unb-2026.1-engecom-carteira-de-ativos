import json

CAPITAL_INICIAL = 100_000.00 # Utiliza _ apenas para separacão visual, o interpretador Python ignora-o completamente
DATA_INICIO = "2025-02-01" # String para comunicar com as API's ao invés de um pd.datetime

BENCHMARKS = {
    "selic": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json",
    "ipca":  "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json",
}

with open("carteira.json", "r", encoding="utf-8") as f:
    CARTEIRA = json.load(f)