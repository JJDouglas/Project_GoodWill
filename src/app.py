import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import dash_table

url = "https://projectgoodwilllink.s3.eu-south-1.amazonaws.com/Tab_macro(inv_divisi)_mod.csv"
url2 = "https://projectgoodwilllink.s3.eu-south-1.amazonaws.com/Tab_macro(lai_divisi).csv"
# Carica il file CSV in un dataframe pandas
df = pd.read_csv(url)
df2 = pd.read_csv(url2)

# Crea l'app Dash
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])
app.title="PROJECT GOODWILL"
server = app.server     # dashtools per il deploy 

# Crea le opzioni del dropdown per year
years = ["Tutti"] + df["Year"].unique().tolist()
dropdown_years = dcc.Dropdown(
    id='dropdown-year',
    options=[{'label': year, 'value': year} for year in years],
    value="Tutti"
)

# Crea le opzioni del dropdown per item name per il primo grafico
names = ["Tutti"] + df["Item name"].unique().tolist()
dropdown_names = dcc.Dropdown(
    id='dropdown-names',
    options=[{'label': name, 'value': name} for name in names],
    value="Tutti"
)

# Crea le opzioni del dropdown per item name per il secondo grafico
names2 = ["Tutti"] + df2["Item name"].unique().tolist()
dropdown_names2 = dcc.Dropdown(
    id='dropdown-names-2',
    options=[{'label': name, 'value': name} for name in names2],
    value="Tutti"
)

# Crea le opzioni del dropdown per Undertaking type
undertakings = ["Tutti"] + df["Undertaking type"].unique().tolist()
dropdown_undertaking = dcc.Dropdown(
    id='dropdown-undertaking',
    options=[{'label': undertaking, 'value': undertaking} for undertaking in undertakings],
    value="Tutti"
)


# Crea il layout dell'app Dash
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("PROJECT GOODWILL"), style={'font-size': 20, 'textAlign': 'center', 'background-color': '#006398', 'color': 'white', 'font-weight': 'bold'})
    ], justify="center"),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.H5("Filtro per anno"),
            dropdown_years
        ], md=3),
        dbc.Col([
            html.H5("Filtro per item name di investments"),
            dropdown_names
        ], md=3),
        dbc.Col([
            html.H5("Filtro per item name di liabilities"),
            dropdown_names2
        ], md=3),
        dbc.Col([
            html.H5("Filtro per undertaking type"),
            dropdown_undertaking
        ], md=3)
    ]),

    dbc.Row([
        dbc.Col([
            #html.H4("Totale investments per Nazione"),
            dcc.Graph(id='pie-chart', style={'width': '600px', 'height': '600px'})
        ], md=6),
        dbc.Col([
            #html.H4("Totale liabilities per Nazione"),
            dcc.Graph(id='pie-chart-2', style={'width': '600px', 'height': '600px'})
        ], md=6)
    ]),

    html.Br(),

], fluid=True)

# Callback per aggiornare i grafici a torta
@app.callback(
    [dash.dependencies.Output('pie-chart', 'figure'),
     dash.dependencies.Output('pie-chart-2', 'figure')],
    [dash.dependencies.Input('dropdown-names', 'value'),
     dash.dependencies.Input('dropdown-names-2', 'value'),
     dash.dependencies.Input('dropdown-undertaking', 'value'),
     dash.dependencies.Input('dropdown-year', 'value')])

def update_pie_chart(name, name2, undertaking, year):
    filtered_df = df
    filtered_df2 = df2

    # Filtra il dataframe in base ai valori dei dropdown
    if name != "Tutti":
        filtered_df = filtered_df[filtered_df["Item name"] == name]
    if name2 != "Tutti":
        filtered_df2 = filtered_df2[filtered_df2["Item name"] == name2]
    if undertaking != "Tutti":
        filtered_df = filtered_df[filtered_df["Undertaking type"] == undertaking]
        filtered_df2 = filtered_df2[filtered_df2["Undertaking type"] == undertaking]
    if year != "Tutti":
        filtered_df = filtered_df[filtered_df["Year"] == year]
        filtered_df2 = filtered_df2[filtered_df2["Year"] == year]

    # Aggrega i dati per Nazione e somma di value di df1
    data = filtered_df.groupby("Country", as_index=False)["Value"].sum()

    # Crea il grafico a torta per gli investimenti
    fig = px.pie(data, values='Value', names='Country', title="ASSET")
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', autosize=False)
    fig.update_yaxes(automargin=True)
    
    # Aggrega i dati per Nazione e somma di Value di df2
    data2 = filtered_df2.groupby("Country", as_index=False)["Value"].sum()

    # Crea il grafico a torta per liabilities
    fig2 = px.pie(data2, values='Value', names='Country', title="LIABILITIES")
    fig2.update_traces(textposition='inside', textinfo='percent+label+value')
    fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', autosize=False)

    return fig, fig2


if __name__ == '__main__':
    app.run_server(debug=True)