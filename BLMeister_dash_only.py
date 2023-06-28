import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import time
# Hier kommen deine Daten und DataFrame
df_eternal = pd.read_csv(r"/Users/joerg/repos/development/blMeister_all_years.csv")
df = df_eternal
app = dash.Dash(__name__)

# Definiere den Layout der Dash-Anwendung
app.layout = html.Div([
    dcc.Slider(
        id='year-slider',
        min=df['Saison'].min(),
        max=df['Saison'].max(),
        value=df['Saison'].min(),
        marks={str(year): str(year) for year in df['Saison'].unique()},
        step=None
    ),
    dcc.Graph(id='bar-chart', style={'height': '1000px'})
])

# Definiere die Callback-Funktion, die aufgerufen wird, wenn sich der Slider ändert
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-slider', 'value')]
)
def update_bar_chart(selected_year):
    # Filtere den DataFrame basierend auf dem ausgewählten Jahr
    selected_row = df[df['Saison'] == selected_year].squeeze()

    # Erstelle die sortierte Liste der Vereine nach Punkten
    data = selected_row[1:].sort_values(ascending=True)
    
    # Filtere die Vereine, deren Punktwerte größer als Null sind
    data = data[data > 0]

    # Anzahl der Balken
    num_bars = len(data)

    # Erstelle das horizontale Balkendiagramm
    fig = go.Figure(data=go.Bar(
        x=data.values,
        y=data.index,
        orientation='h',
        width=0.5,  # Breite der Balken anpassen
        marker=dict(
            color='steelblue',
            line=dict(color='black', width=0.5)
        ),
        # insidetextfont=dict(color='white'),
        # textposition='auto',
        # hovertemplate='%{y}: %{x}',
        # offset=0.05 / num_bars  # Vertikaler Abstand der Balken anpassen
    ))

    # Setze das Layout des Diagramms
    fig.update_layout(
        title=f"Punkteverteilung der Vereine in der Saison {selected_year}",
        xaxis_title="Punktzahl",
        yaxis_title="Verein",
        barmode='group',
        margin={'l': 100, 'r': 100, 't': 50, 'b': 50}
    )

    return fig

# Aktualisiere das Balkendiagramm automatisch mit einer Animation
# @app.callback(
#     Output('bar-chart', 'figure'),
#     [Input('bar-chart', 'id')]
# )

# def animate_bar_chart(value):
#     # Starte mit dem ersten Jahr im DataFrame
#     selected_year = df['Saison'].min()

#     while True:
#         # Aktualisiere das Balkendiagramm für das aktuelle Jahr
#         fig = update_bar_chart(selected_year)

#         # Zeige das Diagramm für eine kurze Zeit an
#         app.renderer.plotlyjs.serve_figures(fig)

#         # Warte für eine Sekunde
#         time.sleep(1)

#         # Inkrementiere das Jahr
#         selected_year += 1

#         # Wenn das Jahr größer als das maximale Jahr im DataFrame ist, setze es auf das minimale Jahr zurück
#         if selected_year > df['Saison'].max():
#             selected_year = df['Saison'].min()

# Starte die Dash-Anwendung
if __name__ == '__main__':
    app.run_server(debug=True)
