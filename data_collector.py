import yfinance as yf
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from config import CARTEIRA, DATA_INICIO, BENCHMARKS

def buscar_renda_variavel(ativo, data_inicio):
    try:
        historico = yf.download(
            ativo["ticker"],
            start=data_inicio,
            progress=False,
            auto_adjust=True,
            multi_level_index=False  # evita MultiIndex que complica o acesso
        )
        time.sleep(1)

        if historico is None or historico.empty:
            print(f"  Aviso: nenhum dado encontrado para {ativo['nome']}")
            return pd.DataFrame()

        preco_inicial = historico["Close"].iloc[0]
        cotas = ativo["valor_investido"] / preco_inicial

        historico = historico.reset_index()
        historico["nome"]          = ativo["nome"]
        historico["tipo"]          = ativo["tipo"]
        historico["valor_inicial"] = ativo["valor_investido"]
        historico["valor_atual"]   = cotas * historico["Close"]

        return historico[["Date", "nome", "tipo", "valor_inicial", "valor_atual"]]

    except Exception as e:
        print(f"  Erro ao coletar {ativo['nome']}: {e}")
        return pd.DataFrame()
    

def simular_renda_fixa(ativo, data_inicio):
    """
    Renda fixa não tem preço de mercado diário.
    Simulamos o crescimento usando juros compostos dia a dia.
    """
    taxa_diaria = (1 + ativo["taxa_anual"]) ** (1/252) - 1 # Essa é a fórmula do juros compostos!
    
    inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    hoje = datetime.today()
    
    datas = []
    valores = []
    data_atual = inicio
    
    while data_atual <= hoje:
        dias = (data_atual - inicio).days
        valor = ativo["valor_investido"] * (1 + taxa_diaria) ** dias
        datas.append(data_atual)
        valores.append(valor)
        data_atual += timedelta(days=1)
        
    return pd.DataFrame({
        "Date": datas,
        "nome": ativo["nome"],
        "tipo": ativo["tipo"],
        "valor_inicial": ativo["valor_investido"],
        "valor_atual": valores,
    })
    
    
def buscar_benchmarks(data_inicio):
    resultado = {}

    # Converte "2025-02-01" → "01/02/2025" (formato que o BCB exige)
    if isinstance(data_inicio, str):
        dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    else:
        dt = data_inicio
    data_bcb = dt.strftime("%d/%m/%Y")

    for nome, url_base in BENCHMARKS.items():
        try:
            url = f"{url_base}&dataInicial={data_bcb}"
            resposta = requests.get(url, timeout=10)
            dados = resposta.json()

            if not isinstance(dados, list) or len(dados) == 0:
                print(f"  Aviso: resposta inesperada para {nome}: {str(dados)[:100]}")
                continue

            df = pd.DataFrame(dados)
            df["data"]  = pd.to_datetime(df["data"], format="%d/%m/%Y")
            df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
            resultado[nome] = df
            print(f"  Benchmark '{nome}': {len(df)} registros coletados")

        except Exception as e:
            print(f"  Erro ao buscar '{nome}': {e}")

    return resultado


def coletar_dados():
    """
    Orquestra as três fontes e retorna um DataFrame unificado
    com todos os ativos e os benchmarks separados.
    """
    inicio = datetime.strptime(DATA_INICIO, "%Y-%m-%d")
    frames = []

    for ativo in CARTEIRA:
        print(f"Coletando: {ativo['nome']}...")

        if ativo["ticker"] is not None:
            df = buscar_renda_variavel(ativo, DATA_INICIO)
        else:
            df = simular_renda_fixa(ativo, DATA_INICIO)

        if not df.empty:
            frames.append(df)

    df_carteira = pd.concat(frames, ignore_index=True)
    df_benchmarks = buscar_benchmarks(inicio)

    return df_carteira, df_benchmarks