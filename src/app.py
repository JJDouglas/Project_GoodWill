import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import dash_table

url = "https://projectgoodwilllink.s3.eu-south-1.amazonaws.com/Tab_macro(inv_divisi)_mod.csv"
url2 = "https://projectgoodwilllink.s3.eu-south-1.amazonaws.com/Tab_macro(lai_divisi).csv"
url3 = "https://projectgoodwilllink.s3.eu-south-1.amazonaws.com/tab_macro+(diviso).csv"
url4 = "https://projectgoodwilllink.s3.eu-south-1.amazonaws.com/df5.csv"

# Caricamento del file CSV in un dataframe pandas
df = pd.read_csv(url) # inv
df2 = pd.read_csv(url2) # lai
df3 = pd.read_csv(url3) # macro
df3.rename(columns={'Somma di Value': 'Value'}, inplace=True)
df4 = pd.read_csv(url4) # table


# Creazione dell'app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title="PROJECT GOODWILL"
server = app.server                     # dashtools per il deploy 

# Creazione del filtro dropdown year
years = ["Tutti"] + df["Year"].unique().tolist()
dropdown_years = dcc.Dropdown(
    id='dropdown-year',
    options=[{'label': year, 'value': year} for year in years],
    value="Tutti",
    clearable=True
)

# Creazione del filtro dropdown item name per il dataset Tab_macro(inv_divisi)
names = ["Tutti"] + df["Item name"].unique().tolist()
dropdown_names = dcc.Dropdown(
    id='dropdown-names',
    options=[{'label': name, 'value': name} for name in names],
    value="Tutti",
    clearable=True
)

# CCreazione del filtro dropdown item name per il dataset Tab_macro(lai_divisi)
names2 = ["Tutti"] + df2["Item name"].unique().tolist()
dropdown_names2 = dcc.Dropdown(
    id='dropdown-names-2',
    options=[{'label': name, 'value': name} for name in names2],
    value="Tutti",
    clearable=True
)

# Crea le opzioni del dropdown per Undertaking type
undertakings = ["Tutti"] + df["Undertaking type"].unique().tolist()
dropdown_undertaking = dcc.Dropdown(
    id='dropdown-undertaking',
    options=[{'label': undertaking, 'value': undertaking} for undertaking in undertakings],
    value="Tutti",
    clearable=True
)


# Aggiunge il terzo grafico a torta al layout dell'app
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
            html.H5("Filtro per item name di assets"),
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
            dcc.Graph(id='pie-chart', style={'width': '600px', 'height': '600px'})
        ], md=4),
        
        dbc.Col([
            dcc.Graph(id='pie-chart-2', style={'width': '600px', 'height': '600px'})
        ], md=4),
        
        dbc.Col([
            dcc.Graph(id='pie-chart-3', style={'width': '600px', 'height': '600px'})
        ], md=4)
    ]),
    
    html.Br(),

], fluid=True)

# Callback per aggiornare i grafici a torta
@app.callback(
    [dash.dependencies.Output('pie-chart', 'figure'),
     dash.dependencies.Output('pie-chart-2', 'figure'),
     dash.dependencies.Output('pie-chart-3', 'figure')],
    [dash.dependencies.Input('dropdown-names', 'value'),
     dash.dependencies.Input('dropdown-names-2', 'value'),
     dash.dependencies.Input('dropdown-undertaking', 'value'),
     dash.dependencies.Input('dropdown-year', 'value')])



# Modifica la funzione update_pie_chart per impostare i colori fissi per ogni Country
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

    # Aggiorna il primo grafico a torta
    fig1 = px.pie(filtered_df, values='Value', names='Country', color='Country', color_discrete_sequence=px.colors.sequential.RdBu, title='<b>'"ASSETS"'<b>')
    fig1.update_traces(textposition='inside', textinfo='percent+label+value')

    # Aggiorna il secondo grafico a torta
    fig2 = px.pie(filtered_df2, values='Value', names='Country', color='Country', color_discrete_sequence=px.colors.sequential.RdBu, title='<b>'"LIABILITIES"'<b>')
    fig2.update_traces(textposition='inside', textinfo='percent+label+value')

    # Calcola la sottrazione tra i valori di value per country dei due grafici a torta
    df_diff = filtered_df.groupby('Country').sum() - filtered_df2.groupby('Country').sum()
    df_diff.reset_index(inplace=True)

    # Aggiungi il terzo grafico a torta con la sottrazione
    fig3 = px.pie(df_diff, values='Value', names='Country', color='Country', color_discrete_sequence=px.colors.sequential.RdBu, title='<b>'"EQUITY"'<b>')
    fig3.update_traces(textposition='inside', textinfo='percent+label+value')

    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)
