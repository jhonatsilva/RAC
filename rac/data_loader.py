import pandas as pd
from .config import SHEET_NAME_BY_YEAR

def load_excel_for_year(filepath: str, year: int) -> pd.DataFrame:
    """Carrega os dados do ano selecionado e normaliza nomes das colunas."""
    if year not in SHEET_NAME_BY_YEAR:
        raise ValueError(f"Ano {year} não configurado.")

    df = pd.read_excel(filepath, sheet_name=SHEET_NAME_BY_YEAR[year])

    # Normaliza nomes das colunas
    df.columns = [c.strip().upper() for c in df.columns]

    # Garante colunas padrão que o sistema usa
    colunas_obrigatorias = ["NATUREZA", "BAIRRO", "HORA", "DIA DA SEMANA", "AMBIENTE", "MÊS"]
    faltando = [c for c in colunas_obrigatorias if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(faltando)}")

    # Limpa e padroniza textos
    for col in ["NATUREZA", "BAIRRO", "DIA DA SEMANA", "AMBIENTE", "MÊS"]:
        df[col] = df[col].astype(str).str.strip().str.upper()

    df["HORA"] = pd.to_numeric(df["HORA"], errors="coerce").fillna(0).astype(int)

    return df
