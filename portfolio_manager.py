import pandas as pd

def calcular_rentabilidade(df_carteira: pd.DataFrame):
    ultimo_dia = df_carteira.groupby("nome").last().reset_index()
    ultimo_dia["rentabilidade_pct"] = (
        (ultimo_dia["valor_atual"] - ultimo_dia["valor_inicial"]) # Diferença do valor atual com o investido
        / ultimo_dia["valor_inicial"] # Divisão pelo valor inicial (total)
    ) * 100 # Multiplicado por 100 para fechar a Regra de 3 e coletando a taxa de rentabilidade
    
    ultimo_dia["ganho_reais"] = ultimo_dia["valor_atual"] - ultimo_dia["valor_inicial"]
    
    return ultimo_dia[["nome", "tipo", "valor_inicial", "valor_atual", "ganho_reais", "rentabilidade_pct"]]


def calcular_resumo_carteira(df_rentabilidade: pd.DataFrame):
    total_inicial = df_rentabilidade["valor_inicial"].sum() # Soma todos os valores iniciais dos ativos (quanto investimos)
    total_atual = df_rentabilidade["valor_atual"].sum() # Soma todos os valores atuais dos ativos (quanto temos após rentabilizar)
    
    rentabilidade_total = ((total_atual - total_inicial) / total_inicial) * 100 # Fórmula que calcula a taxa de rentabilidade de toda a carteira
    
    ganho_total = total_atual - total_inicial
    
    resumo = {
        "capital_inicial": total_inicial,
        "valor_atual": total_atual,
        "ganho_reais": ganho_total,
        "rentabilidade_pct": rentabilidade_total,
    }
    return resumo, df_rentabilidade


def comparar_benchmarks(df_carteira: pd.DataFrame, df_benchmarks: dict):
    ultimo_dia = df_carteira.groupby("nome").last().reset_index()
    total_inicial = ultimo_dia["valor_inicial"].sum()
    total_atual = ultimo_dia["valor_atual"].sum()
    rentabilidade_carteira = ((total_atual - total_inicial) / total_inicial) * 100 # Valor para comparação dentro da função, já que não é passada como parametro
    
    comparacao = {"Carteira": rentabilidade_carteira}
    
    for nome, df in df_benchmarks.items():
        if df.empty: # Valida se o dataframe possui dados
            continue
        
        rentabilidade_acumulada = df["valor"].sum()
        comparacao[nome.upper()] = rentabilidade_acumulada
        
    return comparacao