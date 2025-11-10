import plotly.graph_objs as go


def build_chart(df, meta: dict):
    x = meta.get("x")
    y = meta.get("y")
    title = meta.get("title", "Análise de Ocorrências")
    chart_type = meta.get("type", "bar")

    if x not in df.columns or y not in df.columns:
        raise ValueError(f"Colunas inválidas para o gráfico: x={x}, y={y}")

    x_values = df[x].astype(str).tolist()
    y_values = df[y].tolist()

    color = "#FFD700"  # dourado PMPR

    if chart_type == "bar":
        trace = go.Bar(x=x_values, y=y_values, marker_color=color)
    else:
        trace = go.Scatter(x=x_values, y=y_values, mode="lines+markers", line=dict(color=color, width=3))

    fig = go.Figure(data=[trace])

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(color="#FFD700", size=22, family="Arial Black"),
        ),
        xaxis=dict(title=x, color="white"),
        yaxis=dict(title=y, color="white"),
        template="plotly_dark",
        plot_bgcolor="#1B4332",
        paper_bgcolor="#1B4332",
        font=dict(color="white", family="Segoe UI"),
        margin=dict(l=40, r=20, t=60, b=60),
    )

    return fig.to_plotly_json()
