import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_XLSX = os.path.join(BASE_DIR, "uploads", "Dados_2024-2025 v3.xlsx")


def _detect_col(df, *keywords):
    """
    Encontra a primeira coluna cujo nome contenha TODOS os trechos em keywords.
    Ex: _detect_col(df, "NATUREZA") ou ("BAIRRO",)
    """
    for c in df.columns:
        name = c.upper()
        if all(k in name for k in keywords):
            return c
    return None


def get_filter_values(filepath: str = DEFAULT_XLSX):
    """
    Lê o arquivo padrão e retorna:
      - years: anos únicos
      - crimes: naturezas únicas (ordenadas)
      - bairros: bairros únicos (ordenados)
    Se algo der errado, devolve defaults.
    """
    try:
        if not os.path.exists(filepath):
            print(f"[WARN] Arquivo padrão não encontrado: {filepath}")
            return [2024, 2025], [], []

        df = pd.read_excel(filepath)

        col_ano = _detect_col(df, "ANO")
        col_crime = _detect_col(df, "NATUREZA")
        col_bairro = _detect_col(df, "BAIRRO")

        # anos
        if col_ano:
            years = (
                df[col_ano]
                .dropna()
                .astype(int)
                .drop_duplicates()
                .sort_values()
                .tolist()
            )
        else:
            years = [2024, 2025]

        # crimes
        if col_crime:
            crimes = (
                df[col_crime]
                .dropna()
                .astype(str)
                .str.strip()
                .str.upper()
                .drop_duplicates()
                .sort_values()
                .tolist()
            )
        else:
            crimes = []

        # bairros
        if col_bairro:
            bairros = (
                df[col_bairro]
                .dropna()
                .astype(str)
                .str.strip()
                .str.upper()
                .drop_duplicates()
                .sort_values()
                .tolist()
            )
        else:
            bairros = []

        return years, crimes, bairros

    except Exception as e:
        print(f"[ERRO] get_filter_values: {e}")
        return [2024, 2025], [], []


def load_excel_for_year(filepath: str, year):
    """
    Lê o Excel informado e filtra pelo ano (se houver coluna de ano).
    """
    df = pd.read_excel(filepath)

    col_ano = _detect_col(df, "ANO")
    if col_ano and year:
        df = df[df[col_ano].astype(str) == str(year)]

    return df
