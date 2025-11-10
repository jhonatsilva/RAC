import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from rac.data_loader import get_filter_values, load_excel_for_year
from rac.analysis_functions import run_analysis
from rac.charts import build_chart
from rac.choices import ANALYSIS_OPTIONS

# ==============================
# Configuração básica
# ==============================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"xlsx"}

app = Flask(__name__)
app.secret_key = "segredo_rac_pmpr"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ==============================
# Rota inicial
# ==============================
@app.route("/", methods=["GET"])
def index():
    years, crimes, bairros = get_filter_values()
    return render_template(
        "index.html",
        years=years,
        crimes=crimes,
        bairros=bairros,
        analysis_options=ANALYSIS_OPTIONS,
        error=None,
    )


# ==============================
# Rota de análise
# ==============================
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files.get("file")
        year = request.form.get("year")
        analysis_key = request.form.get("analysis_key")

        crime = (request.form.get("crime") or "").strip() or None
        bairro = (request.form.get("bairro") or "").strip() or None
        semestre = (request.form.get("semestre") or "").strip() or None
        periodo = (request.form.get("periodo") or "").strip() or None

        # Validações básicas
        if not file or file.filename == "":
            flash("Envie um arquivo .xlsx válido.")
            return redirect(url_for("index"))

        if not allowed_file(file.filename):
            flash("Formato inválido. Envie um arquivo .xlsx.")
            return redirect(url_for("index"))

        if not year:
            flash("Selecione o ano.")
            return redirect(url_for("index"))

        if not analysis_key or analysis_key not in ANALYSIS_OPTIONS:
            flash("Selecione um tipo de análise válido.")
            return redirect(url_for("index"))

        # Salvar arquivo
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Carregar base filtrada por ano
        df = load_excel_for_year(filepath, year)
        if df is None or df.empty:
            raise ValueError("Nenhum dado encontrado para o ano selecionado.")

        # Rodar análise
        result_df, meta = run_analysis(
            analysis_key=analysis_key,
            df=df,
            crime=crime,
            bairro=bairro,
            semestre=semestre,
            periodo=periodo,
        )

        # Gerar gráfico
        chart_data = build_chart(result_df, meta)

        return render_template("result.html", chart_data=chart_data, meta=meta)

    except Exception as e:
        print(f"[ERRO] /analyze: {e}")
        flash(f"Erro ao gerar análise: {e}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
