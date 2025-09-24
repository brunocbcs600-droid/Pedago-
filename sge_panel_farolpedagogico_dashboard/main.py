
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import process_data, generate_alerts

st.set_page_config(page_title="Painel SGE - Farol Pedagógico",
                   layout="wide",
                   page_icon="📊")

st.markdown("## 📊 Painel SGE - Farol Pedagógico")
st.markdown("Visual atualizado em estilo dashboard moderno.")

uploaded_file = st.file_uploader("📂 Envie o arquivo .xlsx do SGE", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df_processed = process_data(df)
    alerts = generate_alerts(df_processed)

    # Métricas principais em cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Alunos", df_processed['aluno'].nunique())
    with col2:
        st.metric("Turmas", df_processed['turma'].nunique())
    with col3:
        st.metric("Disciplinas", df_processed['disciplina'].nunique())
    with col4:
        abaixo = (df_processed['media12'] < 6).sum()
        st.metric("Notas abaixo da média", abaixo)

    st.markdown("---")

    # Gráfico circular de classificação dos alunos
    if "classificacao" in df_processed.columns:
        fig_pie = px.pie(df_processed, names="classificacao", title="Distribuição de Classificação")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("### 🔔 Alerta de Alunos com Risco Acadêmico")
    if not alerts.empty:
        st.dataframe(alerts.reset_index(drop=True), height=300)
    else:
        st.success("Nenhum alerta encontrado!")
