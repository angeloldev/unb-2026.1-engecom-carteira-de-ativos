import pandas as pd

def calcular_volatilidade(df_carteira: pd.DataFrame) -> pd.DataFrame:
    resultado = []
    
    for nome, grupo in df_carteira.groupby("nome"):
        retornos_diarios = grupo["valor_atual"].pct_change().dropna()
        volatilidade = retornos_diarios.std() * 100
        resultado.append({
            "nome": nome,
            "volatilidade_pct": round(volatilidade, 4)
        })
        
    return pd.DataFrame(resultado)



def calcular_drawdown(df_carteira: pd.DataFrame) -> pd.DataFrame:
    resultado = []
    
    for nome, grupo in df_carteira.groupby("nome"):
        grupo = grupo.sort_values("Date").reset_index(drop=True)
        pico_acumulado = grupo["valor_atual"].cummax()
        drawdown = (grupo["valor_atual"] - pico_acumulado) / pico_acumulado * 100
        max_drawdown = drawdown.min() # Calcula o menor valor possível (máximo, minimo)
        resultado.append({
            "nome": nome,
            "max_drawdown_pct": round(max_drawdown, 4)
        })
        
    return pd.DataFrame(resultado)



def resumo_risco(df_carteira: pd.DataFrame) -> pd.DataFrame:
    df_vol = calcular_volatilidade(df_carteira)
    df_dd = calcular_drawdown(df_carteira) # dd = DrawDown
    
    return df_vol.merge(df_dd, on="nome")