from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from rac.data_loader import load_excel_for_year
from rac.analysis_functions import run_analysis
from rac.charts import build_chart
from rac.choices import ANALYSIS_OPTIONS

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"xlsx"}

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template(
        "index.html",
        analysis_options=ANALYSIS_OPTIONS
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    # Arquivo
    if "file" not in request.files:
        flash("Selecione um arquivo .xlsx.")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("Nenhum arquivo selecionado.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Formato inválido. Envie um arquivo .xlsx.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Parâmetros básicos
    year = request.form.get("year")
    analysis_key = request.form.get("analysis_key")

    if not year or not analysis_key:
        flash("Selecione o ano e o tipo de análise.")
        return redirect(url_for("index"))

    # Carregar dados do ano
    try:
        df = load_excel_for_year(filepath, int(year))
    except Exception as e:
        flash(f"Erro ao ler o arquivo: {e}")
        return redirect(url_for("index"))

    # Parâmetros adicionais (crime, bairro, semestre, período etc.)
    crime = request.form.get("crime") or None
    bairro = request.form.get("bairro") or None
    semestre = request.form.get("semestre") or None
    periodo = request.form.get("periodo") or None

    # Converter semestre para int se vier preenchido
    if semestre:
        try:
            semestre = int(semestre)
        except ValueError:
            semestre = None

    # Executar análise genérica
    try:
        result_df, meta = run_analysis(
            analysis_key=analysis_key,
            df=df,
            crime=crime,
            bairro=bairro,
            semestre=semestre,
            periodo=periodo
        )
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Erro ao executar análise: {e}")
        return redirect(url_for("index"))

    # Construir gráfico
    chart_json = build_chart(result_df, meta)

    return render_template(
        "result.html",
        chart_json=chart_json,
        meta=meta
    )


if __name__ == "__main__":
    app.run(debug=True)
