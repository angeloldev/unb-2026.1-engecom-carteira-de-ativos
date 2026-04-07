from report_generator import gerar_relatorio_pdf
from portfolio_manager import calcular_rentabilidade, calcular_resumo_carteira, comparar_benchmarks
from analytics import resumo_risco
from data_collector import coletar_dados

df_carteira, df_benchmarks = coletar_dados()

df_rent = calcular_rentabilidade(df_carteira)
resumo, _ = calcular_resumo_carteira(df_rent)
comparacao = comparar_benchmarks(df_carteira, df_benchmarks)

gerar_relatorio_pdf(
    df_carteira=df_carteira,
    df_rentabilidade=df_rent,
    resumo=resumo,
    comparacao=comparacao,
    df_risco=resumo_risco(df_carteira),
    caminho_pdf="relatorio_carteira.pdf"
)