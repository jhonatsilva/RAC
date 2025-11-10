import plotly.graph_objs as go
import numpy as np

def build_chart(df, meta: dict):
    """
    Cria um gráfico Plotly e retorna um dicionário serializável.
    Converte automaticamente arrays numpy em listas.
    """
    x = meta.get("x")
    y = meta.get("y")
    title = meta.get("title", "Gráfico de Análise")
    chart_type = meta.get("type", "bar")

    # Garante que as colunas existem
    if x not in df.columns or y not in df.columns:
        x = df.columns[0]
        y = df.columns[1]

    # Converte arrays numpy -> listas (garantindo compatibilidade com JSON)
    x_values = df[x].tolist() if isinstance(df[x].values, np.ndarray) else df[x]
    y_values = df[y].tolist() if isinstance(df[y].values, np.ndarray) else df[y]

    # Cria o gráfico
    if chart_type == "bar":
        fig = go.Figure([go.Bar(x=x_values, y=y_values)])
    elif chart_type == "line":
        fig = go.Figure([go.Scatter(x=x_values, y=y_values, mode='lines+markers')])
    else:
        fig = go.Figure([go.Bar(x=x_values, y=y_values)])

    # Configura layout
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=60),
    )

    # ✅ Retorna em formato JSON serializável
    return fig.to_plotly_json()
