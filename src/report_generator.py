import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import os

def gerar_grafico_pizza(df_rentabilidade: pd.DataFrame, caminho: str):
    """Composição da carteira por valor investido"""
    labels = df_rentabilidade["nome"].tolist()
    valores = df_rentabilidade["valor_inicial"].tolist()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(valores, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Composição da Carteira", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()


def gerar_grafico_rentabilidade(df_rentabilidade: pd.DataFrame, caminho: str):
    """Barras horizontais — rentabilidade % por ativo"""
    # ordenar do maior para o menor para facilitar leitura
    df = df_rentabilidade.sort_values("rentabilidade_pct")
    
    fig, ax = plt.subplots(figsize=(9, 5))
    cores = ["#d9534f" if v < 0 else "#5cb85c" for v in df["rentabilidade_pct"]]
    ax.barh(df["nome"], df["rentabilidade_pct"], color=cores)
    ax.axvline(x=0, color="black", linewidth=0.8)  # linha vertical no zero
    ax.set_xlabel("Rentabilidade (%)")
    ax.set_title("Rentabilidade por Ativo", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()


def gerar_grafico_evolucao(df_carteira: pd.DataFrame, caminho: str):
    """Linha — evolução do valor total da carteira ao longo do tempo"""
    evolucao = df_carteira.groupby("Date")["valor_atual"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(evolucao["Date"], evolucao["valor_atual"], linewidth=2, color="#337ab7")
    ax.axhline(y=100_000, color="gray", linestyle="--", linewidth=1, label="Capital inicial")
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor (R$)")
    ax.set_title("Evolução da Carteira", fontsize=14, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()


def gerar_grafico_benchmark(comparacao: dict, caminho: str):
    """Barras agrupadas — carteira vs benchmarks"""
    nomes = list(comparacao.keys())
    valores = list(comparacao.values())
    cores = ["#337ab7" if n == "Carteira" else "#aaaaaa" for n in nomes]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(nomes, valores, color=cores)
    ax.set_ylabel("Rentabilidade acumulada (%)")
    ax.set_title("Carteira vs Benchmarks", fontsize=14, fontweight="bold")
    for i, v in enumerate(valores):
        ax.text(i, v + 0.2, f"{v:.1f}%", ha="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close()
    
def gerar_relatorio_pdf(df_carteira, df_rentabilidade, resumo, comparacao, df_risco, caminho_pdf="relatorio.pdf"):
    os.makedirs("graficos", exist_ok=True)
    p_pizza = "graficos/pizza.png"
    p_rent = "graficos/rentabilidade.png"
    p_evolucao = "graficos/evolucao.png"
    p_benchmark = "graficos/benchmark.png"
    
    gerar_grafico_pizza(df_rentabilidade, p_pizza)
    gerar_grafico_rentabilidade(df_rentabilidade, p_rent)
    gerar_grafico_evolucao(df_carteira, p_evolucao)
    gerar_grafico_benchmark(comparacao, p_benchmark)
    
    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    estilos = getSampleStyleSheet()
    elementos = []
    
    elementos.append(Paragraph("Carteira de Investimentos", estilos["Title"]))
    elementos.append(Paragraph("Relatório de Desempenho — Engenharia Econômica", estilos["Normal"]))
    elementos.append(Spacer(1, 0.5*cm))
    
    elementos.append(Paragraph("Resumo da Carteira", estilos["Heading2"]))
    dados_tabela = [
        ["Capital Inicial", "Valor Atual", "Ganho (R$)", "Rentabilidade"],
        [
            f"R$ {resumo['capital_inicial']:,.2f}",
            f"R$ {resumo['valor_atual']:,.2f}",
            f"R$ {resumo['ganho_reais']:,.2f}",
            f"{resumo['rentabilidade_pct']:.2f}%"
        ]
    ]
    tabela = Table(dados_tabela, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#337ab7")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.white]),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 0.5*cm))
    
    for titulo, caminho in [
        ("Composição da Carteira", p_pizza),
        ("Rentabilidade por Ativo", p_rent),
        ("Evolução da Carteira", p_evolucao),
        ("Carteira vs Benchmarks", p_benchmark),
    ]:
        elementos.append(Paragraph(titulo, estilos["Heading2"]))
        elementos.append(Image(caminho, width=16*cm, height=9*cm))
        elementos.append(Spacer(1, 0.3*cm))
        
    doc.build(elementos)
    print(f"Relatório gerado: {caminho_pdf}")