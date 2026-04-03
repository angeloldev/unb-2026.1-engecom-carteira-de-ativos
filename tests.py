from analytics import resumo_risco
from data_collector import coletar_dados

df_carteira, _ = coletar_dados()
df_risco = resumo_risco(df_carteira)
print("\n=== ANÁLISE DE RISCO ===")
print(df_risco.to_string(index=False))