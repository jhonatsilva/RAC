import pandas as pd

# ===================== CONFIGURAÇÕES DE BASE ===================== #
CRIMES_PERIGOSOS = [
    "FURTO SIMPLES",
    "FURTO QUALIFICADO",
    "ROUBO",
    "ROUBO AGRAVADO",
    "ROUBO COM RESULTADO DE LESAO CORPORAL GRAVE",
    "EXTORSAO MEDIANTE SEQUESTRO",
    "DROGAS PARA O CONSUMO PESSOAL",
    "PORTE ILEGAL DE ARMA DE FOGO, ACESSORIO OU MUNICAO - USO PERMITIDO",
    "COMERCIO ILEGAL DE ARMA DE FOGO",
    "VIOLACAO DE DOMICILIO",
    "FURTO DE COISA COMUM",
    "DANO",
]

FURTOS = ["FURTO SIMPLES", "FURTO QUALIFICADO", "FURTO DE COISA COMUM"]
ROUBOS = ["ROUBO", "ROUBO AGRAVADO", "ROUBO COM RESULTADO DE LESAO CORPORAL GRAVE"]
FURTOS_ROUBOS = FURTOS + ROUBOS

CRIMES_COMERCIO = [
    "FURTO SIMPLES", "FURTO QUALIFICADO", "ROUBO",
    "ROUBO AGRAVADO", "ROUBO COM RESULTADO DE LESAO CORPORAL GRAVE",
    "DANO", "VIOLACAO DE DOMICILIO", "FURTO DE COISA COMUM"
]

MES_MAP = {
    "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4,
    "MAI": 5, "JUN": 6, "JUL": 7, "AGO": 8,
    "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12
}


def _periodo(hora: int) -> str:
    """Classifica a hora em período."""
    try:
        h = int(hora)
    except (TypeError, ValueError):
        return "INDEFINIDO"
    if 6 <= h <= 11:
        return "MANHÃ"
    elif 12 <= h <= 17:
        return "TARDE"
    else:
        return "NOITE"


# ===================== FUNÇÕES PRINCIPAIS ===================== #

def ocorrencias_filtro_crime(df: pd.DataFrame, crime: str):
    f = df[df["NATUREZA"] == crime.upper()]
    res = f["NATUREZA"].value_counts().reset_index()
    res.columns = ["Natureza", "Quantidade"]
    meta = {
        "title": f"Total de ocorrências - {crime.upper()}",
        "x": "Natureza", "y": "Quantidade", "type": "bar"
    }
    return res, meta


def ranking_bairros_crime(df: pd.DataFrame, crime: str):
    f = df[df["NATUREZA"] == crime.upper()]
    res = f["BAIRRO"].value_counts().reset_index(name="Crimes").head(20)
    res.columns = ["Bairro", "Crimes"]
    meta = {
        "title": f"Top 20 bairros - {crime.upper()}",
        "x": "Bairro", "y": "Crimes", "type": "bar"
    }
    return res, meta


def crimes_dia_crime_bairro(df: pd.DataFrame, crime: str, bairro: str):
    f = df[(df["NATUREZA"] == crime.upper()) & (df["BAIRRO"] == bairro.upper())]
    res = f["DIA DA SEMANA"].value_counts().reset_index(name="Quantidade")
    res.columns = ["Dia da Semana", "Quantidade"]
    meta = {
        "title": f"{crime.upper()} em {bairro.upper()} por dia da semana",
        "x": "Dia da Semana", "y": "Quantidade", "type": "bar"
    }
    return res, meta


def periodo_crime_bairro(df: pd.DataFrame, crime: str, bairro: str):
    f = df[(df["NATUREZA"] == crime.upper()) & (df["BAIRRO"] == bairro.upper())].copy()
    f["PERIODO"] = f["HORA"].apply(_periodo)
    res = f["PERIODO"].value_counts().reset_index(name="Quantidade")
    res.columns = ["Período", "Quantidade"]
    meta = {
        "title": f"{crime.upper()} em {bairro.upper()} por período",
        "x": "Período", "y": "Quantidade", "type": "bar"
    }
    return res, meta


def crimes_perigosos_semestre(df: pd.DataFrame, semestre: int):
    f = df[df["NATUREZA"].isin(CRIMES_PERIGOSOS)].copy()
    f["MES_NUM"] = f["MÊS"].map(MES_MAP)

    if semestre == 1:
        f = f[f["MES_NUM"].between(1, 6)]
    else:
        f = f[f["MES_NUM"].between(7, 12)]

    res = f.groupby("MÊS").size().reset_index(name="Crimes").sort_values("Crimes", ascending=False)
    meta = {
        "title": f"Crimes perigosos - {semestre}º semestre",
        "x": "MÊS", "y": "Crimes", "type": "bar"
    }
    return res, meta


def crimes_moradias_semestre(df: pd.DataFrame, semestre: int):
    base = df.copy()
    viol = base[(base["NATUREZA"] == "VIOLACAO DE DOMICILIO") & (base["AMBIENTE"] == "RESIDENCIA")]
    dano = base[(base["NATUREZA"] == "DANO") & (base["AMBIENTE"] == "RESIDENCIA")]
    fr = base[(base["NATUREZA"].isin(FURTOS_ROUBOS)) & (base["AMBIENTE"] == "RESIDENCIA")]

    allc = pd.concat([viol, dano, fr])
    allc["MES_NUM"] = allc["MÊS"].map(MES_MAP)
    if semestre == 1:
        allc = allc[allc["MES_NUM"].between(1, 6)]
    else:
        allc = allc[allc["MES_NUM"].between(7, 12)]

    res = allc.groupby("MÊS").size().reset_index(name="Crimes").sort_values("Crimes", ascending=False)
    meta = {
        "title": f"Crimes contra moradias - {semestre}º semestre",
        "x": "MÊS", "y": "Crimes", "type": "bar"
    }
    return res, meta


def crimes_moradias_bairro(df: pd.DataFrame, bairro: str):
    base = df.copy()
    viol = base[(base["NATUREZA"] == "VIOLACAO DE DOMICILIO") & (base["AMBIENTE"] == "RESIDENCIA")]
    dano = base[(base["NATUREZA"] == "DANO") & (base["AMBIENTE"] == "RESIDENCIA")]
    fr = base[(base["NATUREZA"].isin(FURTOS_ROUBOS)) & (base["AMBIENTE"] == "RESIDENCIA")]
    allc = pd.concat([viol, dano, fr])
    b = allc[allc["BAIRRO"] == bairro.upper()]
    res = b["NATUREZA"].value_counts().reset_index(name="Crimes")
    res.columns = ["Natureza", "Crimes"]
    meta = {
        "title": f"Crimes em moradias - {bairro.upper()}",
        "x": "Natureza", "y": "Crimes", "type": "bar"
    }
    return res, meta


def periodo_moradias_bairro(df: pd.DataFrame, bairro: str):
    base = df.copy()
    base["PERIODO"] = base["HORA"].apply(_periodo)
    f = base[(base["BAIRRO"] == bairro.upper()) & (base["AMBIENTE"] == "RESIDENCIA")]
    res = f["PERIODO"].value_counts().reset_index(name="Crimes")
    res.columns = ["Período", "Crimes"]
    meta = {
        "title": f"Período - crimes em moradias ({bairro.upper()})",
        "x": "Período", "y": "Crimes", "type": "bar"
    }
    return res, meta


def dia_moradias_bairro(df: pd.DataFrame, bairro: str):
    f = df[(df["BAIRRO"] == bairro.upper()) & (df["AMBIENTE"] == "RESIDENCIA")]
    res = f["DIA DA SEMANA"].value_counts().reset_index(name="Crimes")
    res.columns = ["Dia da Semana", "Crimes"]
    meta = {
        "title": f"Dia da semana - crimes em moradias ({bairro.upper()})",
        "x": "Dia da Semana", "y": "Crimes", "type": "bar"
    }
    return res, meta


def periodo_furtos_roubos_bairro(df: pd.DataFrame, bairro: str):
    f = df[(df["BAIRRO"] == bairro.upper()) & (df["NATUREZA"].isin(FURTOS_ROUBOS))].copy()
    f["PERIODO"] = f["HORA"].apply(_periodo)
    cont = f.groupby(["NATUREZA", "PERIODO"]).size().reset_index(name="Ocorrências")
    idx = cont.groupby("NATUREZA")["Ocorrências"].idxmax()
    principal = cont.loc[idx].sort_values("Ocorrências", ascending=False)
    meta = {
        "title": f"Período principal - furtos/roubos ({bairro.upper()})",
        "x": "NATUREZA", "y": "Ocorrências", "type": "bar"
    }
    return principal.rename(columns={"NATUREZA": "Natureza"}), meta


def dia_furtos_roubos_bairro(df: pd.DataFrame, bairro: str):
    f = df[(df["BAIRRO"] == bairro.upper()) & (df["NATUREZA"].isin(FURTOS_ROUBOS))]
    cont = f.groupby(["NATUREZA", "DIA DA SEMANA"]).size().reset_index(name="Ocorrências")
    idx = cont.groupby("NATUREZA")["Ocorrências"].idxmax()
    principal = cont.loc[idx].sort_values("Ocorrências", ascending=False)
    meta = {
        "title": f"Dia principal - furtos/roubos ({bairro.upper()})",
        "x": "NATUREZA", "y": "Ocorrências", "type": "bar"
    }
    return principal.rename(columns={"NATUREZA": "Natureza"}), meta


def periodo_crime_bairro_resumo(df: pd.DataFrame, bairro: str):
    f = df[df["BAIRRO"] == bairro.upper()][["HORA", "NATUREZA"]].copy()
    f["PERIODO"] = f["HORA"].apply(_periodo)
    cont = f.value_counts(["NATUREZA", "PERIODO"]).reset_index(name="Contagem")
    idx = cont.groupby("NATUREZA")["Contagem"].idxmax()
    principal = cont.loc[idx].sort_values("Contagem", ascending=False)
    meta = {
        "title": f"Período principal por crime ({bairro.upper()})",
        "x": "NATUREZA", "y": "Contagem", "type": "bar"
    }
    return principal.rename(columns={"NATUREZA": "Natureza"}), meta


def crimes_perigosos_bairro_periodo(df: pd.DataFrame, bairro: str, periodo: str):
    f = df[df["NATUREZA"].isin(CRIMES_PERIGOSOS)].copy()
    f["PERIODO"] = f["HORA"].apply(_periodo)
    f = f[(f["BAIRRO"] == bairro.upper()) & (f["PERIODO"] == periodo.upper())]
    res = f["NATUREZA"].value_counts().reset_index(name="Crimes")
    res.columns = ["Natureza", "Crimes"]
    meta = {
        "title": f"Crimes perigosos em {bairro.upper()} ({periodo.upper()})",
        "x": "Natureza", "y": "Crimes", "type": "bar"
    }
    return res, meta


def crime_comercial_bairro(df: pd.DataFrame, bairro: str):
    f = df[df["NATUREZA"].isin(CRIMES_COMERCIO)].copy()
    f = f[(f["HORA"].between(8, 18)) & (f["AMBIENTE"] == "COMERCIO") & (f["BAIRRO"] == bairro.upper())]
    res = f["NATUREZA"].value_counts().reset_index(name="Crimes")
    res.columns = ["Natureza", "Crimes"]
    meta = {
        "title": f"Crimes em comércio - horário comercial ({bairro.upper()})",
        "x": "Natureza", "y": "Crimes", "type": "bar"
    }
    return res, meta


# ===================== DESPACHANTE ===================== #

def run_analysis(analysis_key: str, df: pd.DataFrame,
                 crime=None, bairro=None, semestre=None, periodo=None):
    """Executa a função correta conforme o tipo de análise."""

    if analysis_key == "ocorrencias_filtro_crime":
        return ocorrencias_filtro_crime(df, crime)
    if analysis_key == "ranking_bairros_crime":
        return ranking_bairros_crime(df, crime)
    if analysis_key == "crimes_dia_crime_bairro":
        return crimes_dia_crime_bairro(df, crime, bairro)
    if analysis_key == "periodo_crime_bairro":
        return periodo_crime_bairro(df, crime, bairro)
    if analysis_key == "crimes_perigosos_semestre":
        return crimes_perigosos_semestre(df, int(semestre))
    if analysis_key == "crimes_moradias_semestre":
        return crimes_moradias_semestre(df, int(semestre))
    if analysis_key == "crimes_moradias_bairro":
        return crimes_moradias_bairro(df, bairro)
    if analysis_key == "periodo_moradias_bairro":
        return periodo_moradias_bairro(df, bairro)
    if analysis_key == "dia_moradias_bairro":
        return dia_moradias_bairro(df, bairro)
    if analysis_key == "periodo_furtos_roubos_bairro":
        return periodo_furtos_roubos_bairro(df, bairro)
    if analysis_key == "dia_furtos_roubos_bairro":
        return dia_furtos_roubos_bairro(df, bairro)
    if analysis_key == "periodo_crime_bairro_resumo":
        return periodo_crime_bairro_resumo(df, bairro)
    if analysis_key == "crimes_perigosos_bairro_periodo":
        return crimes_perigosos_bairro_periodo(df, bairro, periodo)
    if analysis_key == "crime_comercial_bairro":
        return crime_comercial_bairro(df, bairro)

    raise ValueError("Tipo de análise inválido ou não implementado.")
