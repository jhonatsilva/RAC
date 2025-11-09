# RAC - Raio-X das Ocorrências Criminais em CWB

Sistema web simples e funcional para análise de ocorrências criminais em Curitiba,
baseado em planilhas oficiais (ex.: `CTBA_2024`, `CTBA_2025`) e visualização gráfica.

## Tecnologias

- Python 3.10+ (recomendado)
- Flask (backend e rotas)
- Pandas (leitura e tratamento dos dados)
- openpyxl (leitura de arquivos .xlsx)
- Plotly (gráficos interativos no navegador)
- Gunicorn (opcional, para deploy em produção)
- python-dotenv (opcional, para variáveis de ambiente)

## Estrutura de Pastas

```bash
RAC/
├─ app.py
├─ requirements.txt
├─ README.md
├─ rac/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ data_loader.py
│  ├─ analysis_functions.py
│  ├─ charts.py
│  └─ choices.py
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  └─ result.html
└─ static/
   ├─ css/
   │  └─ style.css
   └─ js/
      └─ main.js
Instalação
Clone ou copie o projeto:

git clone <seu-repo-ou-pasta> RAC
cd RAC
Crie e ative um ambiente virtual (opcional, mas recomendado):

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
Instale as dependências:

pip install -r requirements.txt
Se preferir instalar manualmente:

pip install flask pandas openpyxl plotly python-dotenv
Execute a aplicação:

python app.py
Acesse no navegador:

Uso
Na página inicial:

Selecione o arquivo .xlsx com as abas CTBA_2024, CTBA_2025, etc.

Escolha o ano da análise.

Escolha o tipo de análise na lista (ex.: ranking de bairros por crime).

Informe parâmetros adicionais quando solicitado (crime, bairro, semestre, período, etc).

A aplicação irá:

Ler os dados do ano selecionado.

Executar a função correspondente.

Exibir o gráfico em uma nova página dedicada.

Disponibilizar um botão "Voltar" para retornar à tela inicial e escolher outra análise.

Observações
Estrutura preparada para você adicionar novas funções facilmente.

Todas as regras de negócio e filtros ficam em rac/analysis_functions.py.

Toda a parte visual em templates/ e static/.

---

## 2. `requirements.txt`

```txt
flask
pandas
openpyxl
plotly
python-dotenv
