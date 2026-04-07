# teste.py
from src.data_collector import coletar_dados

df_carteira, df_benchmarks = coletar_dados()

print("\n=== CARTEIRA ===")
print(df_carteira.head(10))
print(f"\nTotal de linhas: {len(df_carteira)}")
print(f"Ativos coletados: {df_carteira['nome'].unique()}")

print("\n=== BENCHMARKS ===")
for nome, df in df_benchmarks.items():
    print(f"{nome}: {len(df)} registros")