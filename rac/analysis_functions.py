import pandas as pd


def _detect_col(df, *keywords):
    for c in df.columns:
        name = c.upper()
        if all(k in name for k in keywords):
            return c
    return None


def definir_periodo(valor):
    try:
        s = str(valor)
        if ":" in s:
            h = int(s.split(":")[0])
        else:
            h = int(float(s))
    except Exception:
        return "INDEFINIDO"

    if 5 <= h < 12:
        return "MANHÃ"
    if 12 <= h < 18:
        return "TARDE"
    if 18 <= h <= 23:
        return "NOITE"
    return "MADRUGADA"


def run_analysis(analysis_key, df, crime=None, bairro=None, semestre=None, periodo=None):
    # detectar colunas
    col_crime = _detect_col(df, "NATUREZA")
    col_bairro = _detect_col(df, "BAIRRO")
    col_mes = _detect_col(df, "MES") or _detect_col(df, "MÊS")
    col_hora = _detect_col(df, "HORA")

    # normalizar filtros
    crime = crime.strip().upper() if crime else None
    bairro = bairro.strip().upper() if bairro else None

    dff = df.copy()

    # ================= TOTAL POR CRIME =================
    if analysis_key == "total_por_crime":
        if not col_crime:
            raise ValueError("Coluna de crime (NATUREZA) não encontrada na base.")
        if crime:
            dff = dff[dff[col_crime].astype(str).str.upper() == crime]

        result = (
            dff.groupby(col_crime)
            .size()
            .reset_index(name="TOTAL")
            .sort_values("TOTAL", ascending=False)
        )

        title = "Total de ocorrências por crime"
        if crime:
            title += f" - filtrado em {crime}"

        return result, {"title": title, "x": col_crime, "y": "TOTAL", "type": "bar"}

    # ================= TOTAL POR BAIRRO =================
    if analysis_key == "total_por_bairro":
        if not col_bairro:
            raise ValueError("Coluna BAIRRO não encontrada na base.")
        if bairro:
            dff = dff[dff[col_bairro].astype(str).str.upper() == bairro]

        result = (
            dff.groupby(col_bairro)
            .size()
            .reset_index(name="TOTAL")
            .sort_values("TOTAL", ascending=False)
        )

        title = "Total de ocorrências por bairro"
        if bairro:
            title += f" - apenas " + bairro

        return result, {"title": title, "x": col_bairro, "y": "TOTAL", "type": "bar"}

    # ========== CRIME POR BAIRRO (crime obrigatório) ==========
    if analysis_key == "crime_por_bairro":
        if not col_crime or not col_bairro:
            raise ValueError("Colunas NATUREZA e BAIRRO são necessárias.")
        if not crime:
            raise ValueError("Selecione um crime para esta análise.")

        dff = dff[dff[col_crime].astype(str).str.upper() == crime]

        result = (
            dff.groupby(col_bairro)
            .size()
            .reset_index(name="TOTAL")
            .sort_values("TOTAL", ascending=False)
        )

        return result, {
            "title": f"Distribuição do crime {crime} por bairro",
            "x": col_bairro,
            "y": "TOTAL",
            "type": "bar",
        }

    # ========== BAIRRO POR CRIME (bairro obrigatório) ==========
    if analysis_key == "bairro_por_crime":
        if not col_crime or not col_bairro:
            raise ValueError("Colunas NATUREZA e BAIRRO são necessárias.")
        if not bairro:
            raise ValueError("Selecione um bairro para esta análise.")

        dff = dff[dff[col_bairro].astype(str).str.upper() == bairro]

        result = (
            dff.groupby(col_crime)
            .size()
            .reset_index(name="TOTAL")
            .sort_values("TOTAL", ascending=False)
        )

        return result, {
            "title": f"Distribuição de crimes no bairro {bairro}",
            "x": col_crime,
            "y": "TOTAL",
            "type": "bar",
        }

    # ========== COMPARATIVO SEMESTRE ==========
    if analysis_key == "comparativo_semestre":
        if not col_mes:
            raise ValueError("Coluna de mês não encontrada na base.")

        def _sem(m):
            try:
                m = int(m)
                return 1 if m <= 6 else 2
            except Exception:
                return None

        dff["SEMESTRE"] = dff[col_mes].apply(_sem)
        dff = dff[dff["SEMESTRE"].notna()]

        result = (
            dff.groupby("SEMESTRE")
            .size()
            .reset_index(name="TOTAL")
            .sort_values("SEMESTRE")
        )

        return result, {
            "title": "Comparativo de ocorrências por semestre",
            "x": "SEMESTRE",
            "y": "TOTAL",
            "type": "bar",
        }

    # ========== PERÍODO DO DIA ==========
    if analysis_key == "periodo_dia":
        if not col_hora:
            raise ValueError("Coluna de hora não encontrada na base.")

        dff["PERIODO"] = dff[col_hora].apply(definir_periodo)

        result = (
            dff.groupby("PERIODO")
            .size()
            .reset_index(name="TOTAL")
            .sort_values("TOTAL", ascending=False)
        )

        return result, {
            "title": "Distribuição das ocorrências por período do dia",
            "x": "PERIODO",
            "y": "TOTAL",
            "type": "bar",
        }

    # ========== GERAL ==========
    if analysis_key == "geral":
        total = len(dff)
        crimes = dff[col_crime].nunique() if col_crime else 0
        bairros = dff[col_bairro].nunique() if col_bairro else 0

        resumo = pd.DataFrame(
            {
                "Indicador": [
                    "Total de ocorrências",
                    "Tipos de crime distintos",
                    "Bairros com registros",
                ],
                "Valor": [total, crimes, bairros],
            }
        )

        return resumo, {
            "title": "Resumo geral das ocorrências",
            "x": "Indicador",
            "y": "Valor",
            "type": "bar",
        }

    raise ValueError("Tipo de análise inválido ou não implementado.")
