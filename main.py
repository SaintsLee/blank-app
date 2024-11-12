import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.colors as pc
st.set_page_config(layout="wide", page_title="Estudo Usufruto",page_icon = "portfel_logo.ico")
st.markdown(
    """
    <style>
    body {
        margin-top: -20px;  /* Diminui a margem superior da página */
    }
    </style>
    """,
    unsafe_allow_html=True
)
@st.cache_data
def load_data():
    dados_completos = pd.read_parquet("dados_completos_brotli.parquet")
    dados_completos_retornos = pd.read_parquet("dados_completos__retornos_brotli.parquet")
    return dados_completos, dados_completos_retornos
dados_completos, dados_completos_retornos = load_data()
st.title("Análise do patrimônio final")
st.markdown(
    """
    <style>
    /* Remover o valor abaixo do slider*/
    .st-emotion-cache-hpex6h.ew7r33m0
    {
        visibility: hidden;
    }
    /* Diminuir o espaço entre os widgets */
    .stElementContainer.element-container.st-emotion-cache-1jm780e.e1f1d6gn4 { 
     /* O seletor CSS para widgets em Streamlit */
        margin-bottom: 0px;  /* Ajuste o valor para diminuir o espaço */
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
def calcula_drawdown(dataset):
    retornos = dataset.cummax()
    drawdowns = dataset / retornos - 1
    drawdown_max = drawdowns.min()
    return drawdowns, drawdown_max

def calcula_retornos(dados_completos_retornos, periodo_carteira, nomes_carteiras, opcao):
    retornos_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
    if opcao == 1:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().max(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos
    elif opcao == 2:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[
                (dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                    0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().min(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos
    elif opcao == 3:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[
                (dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                    0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().median(axis = 0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos
    elif opcao == 4:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[
                (dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                    0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().mean(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos

	@@ -290,14 +287,10 @@ def desenha_linha_formatado(dataset, titulo_y, titulo_x):
                     "Média de todas as carteiras": 4}

    opcao_radio1 = st.radio("Opções interessantes para análise:", list(opcoes_label1.keys()),label_visibility="hidden")
    retornos = calcula_retornos(dados_completos_retornos, periodo_carteira, nomes_carteiras, opcoes_label1[opcao_radio1])

    st.markdown(
        """
        <div style="margin-top: 77px;"></div>
        """,
        unsafe_allow_html=True
    )

    box_plot_3 = desenha_box_formatado(retornos*100, "Retornos [%]", "Carteiras")
    st.plotly_chart(box_plot_3, use_container_width=False)
    #_______________________________________________________
with col2:
    # Box Plot 2 - Disperssão do Drawdown
    draw_downs_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
    for i in range(len(nomes_carteiras)):
        dd, mdd = calcula_drawdown(
            dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                     & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[0])].drop(
                columns=["Carteira", "Periodo"])
            )
        draw_downs_totais[nomes_carteiras[i].split()[0]] = mdd
    box_plot_2 = desenha_box_formatado(draw_downs_totais * 100, "Drawdown [%]", "Carteiras")
    st.markdown("#### Dispersão do Drawdown")
    st.write("Taxa: {:.2f}%".format(taxa_carteira))
    st.plotly_chart(box_plot_2, use_container_width=False)
    #_______________________________________________________
    # Box Plot 4 - Disperssão da Volatilidade
    st.markdown("#### Volatilidade das carteiras")
    opcoes_label2 = {"Carteira com maior volatilidade": 1,
                     "Carteira com menor volatilidade": 2,
                     "Mediana":                         3,
                     "Média de todas as carteiras":     4}
    opcao_radio2 = st.radio("Opções interessantes para análise:", list(opcoes_label2.keys()),label_visibility="hidden")
    janela_analise = st.slider("# Período da volatilidade móvel [meses]", 2, 24, 2, 1)
    volatilidade = calcula_volatilidade(dados_completos_retornos,
                                        periodo_carteira,
                                        nomes_carteiras,
                                        janela_analise,
                                        opcoes_label2[opcao_radio2])
    box_plot_4 = desenha_linha_formatado(volatilidade*100, "Retornos [%]", "Carteiras")
    st.plotly_chart(box_plot_4, use_container_width=False)
    #_______________________________________________________
