ANALYSIS_OPTIONS = {
    "total_por_crime": {
        "label": "Total de ocorrências por crime",
        "params": ["crime"]       # crime opcional (vazio = todos)
    },
    "total_por_bairro": {
        "label": "Total de ocorrências por bairro",
        "params": ["bairro"]      # bairro opcional (vazio = todos)
    },
    "crime_por_bairro": {
        "label": "Ocorrências por bairro de um crime específico",
        "params": ["crime", "bairro"]  # crime obrigatório, bairro opcional (ou todos)
    },
    "bairro_por_crime": {
        "label": "Ocorrências por crime em um bairro específico",
        "params": ["bairro", "crime"]  # bairro obrigatório, crime opcional (ou todos)
    },
    "comparativo_semestre": {
        "label": "Comparativo entre semestres",
        "params": []              # sem filtro manual
    },
    "periodo_dia": {
        "label": "Distribuição por período do dia",
        "params": []              # aqui vamos por período calculado, não input fixo
    },
    "geral": {
        "label": "Resumo geral da base",
        "params": []
    }
}
