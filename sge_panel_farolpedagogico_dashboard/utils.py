
import pandas as pd

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # Renomeia colunas para padrão esperado
    df = df.rename(columns=lambda x: x.strip().lower())
    if "nota 1" in df.columns:
        df = df.rename(columns={"nota 1": "n1"})
    if "nota 2" in df.columns:
        df = df.rename(columns={"nota 2": "n2"})
    if "aluno" not in df.columns and "nome" in df.columns:
        df = df.rename(columns={"nome": "aluno"})

    # Calcula média
    if "n1" in df.columns and "n2" in df.columns:
        df["media12"] = (df["n1"] + df["n2"]) / 2

    # Classificação
    if "media12" in df.columns:
        df["classificacao"] = df["media12"].apply(lambda x: "Abaixo da Média" if x < 6 else "Acima da Média")

    return df

def generate_alerts(df: pd.DataFrame) -> pd.DataFrame:
    if "media12" in df.columns:
        return df[df["media12"] < 6][["aluno","turma","disciplina","n1","n2","media12","classificacao"]]
    return pd.DataFrame()
