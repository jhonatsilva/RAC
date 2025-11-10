from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd

from rac.data_loader import load_excel_for_year
from rac.analysis_functions import run_analysis
from rac.charts import build_chart
from rac.choices import ANALYSIS_OPTIONS

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"xlsx"}

app = Flask(__name__)
app.secret_key = "secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Armazenamento temporário de dados carregados
datasets = {}


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", analysis_options=ANALYSIS_OPTIONS)


@app.route("/load-options", methods=["POST"])
def load_options():
    """Retorna listas únicas de valores (crimes, bairros etc.) com base no arquivo e ano."""
    file = request.files.get("file")
    year = request.form.get("year")

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Arquivo inválido."}), 400

    try:
        year = int(year)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        df = load_excel_for_year(filepath, year)
        datasets["df"] = df  # salva temporariamente

        crimes = sorted(df["NATUREZA"].unique().tolist())
        bairros = sorted(df["BAIRRO"].unique().tolist())
        semestres = [1, 2]
        periodos = ["MANHÃ", "TARDE", "NOITE"]

        return jsonify({
            "crimes": crimes,
            "bairros": bairros,
            "semestres": semestres,
            "periodos": periodos
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze", methods=["POST"])
def analyze():
    """Executa a análise e retorna o gráfico."""
    df = datasets.get("df")
    if df is None:
        flash("Nenhum dataset carregado.")
        return redirect(url_for("index"))

    analysis_key = request.form.get("analysis_key")
    crime = request.form.get("crime")
    bairro = request.form.get("bairro")
    semestre = request.form.get("semestre")
    periodo = request.form.get("periodo")

    try:
        if semestre:
            semestre = int(semestre)
        result_df, meta = run_analysis(
            analysis_key=analysis_key,
            df=df,
            crime=crime,
            bairro=bairro,
            semestre=semestre,
            periodo=periodo
        )
        chart_json = build_chart(result_df, meta)
        return render_template("result.html", chart_json=chart_json, meta=meta)
    except Exception as e:
        flash(f"Erro ao gerar gráfico: {e}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
