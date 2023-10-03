import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import time

# Hier kommen deine Daten und DataFrame
df = pd.read_csv(r"/Users/joerg/repos/development/blMeister_all_years.csv")

# Erstelle eine Dash-Anwendung
app = dash.Dash(__name__)

# Definiere den Layout der Dash-Anwendung
app.layout = html.Div([
    dcc.Graph(id='bar-chart', style={'height': '800px'}),
])

# Definiere die Funktion zum Aktualisieren des Balkendiagramms
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('bar-chart', 'id')]
)
def update_bar_chart(selected_year):
    # Filtere den DataFrame basierend auf dem ausgewählten Jahr
    selected_row = df[df['Saison'] == selected_year].squeeze()

    # Erstelle die sortierte Liste der Vereine nach Punkten
    data = selected_row[2:].sort_values(ascending=False)

    # Filtere die Vereine, deren Punktwerte größer als Null sind
    data = data[data > 0]

    # Erstelle das horizontale Balkendiagramm
    fig = go.Figure(data=go.Bar(
        x=data.values,
        y=data.index,
        orientation='h',
        width=0.5,  # Breite der Balken anpassen
        marker=dict(
            color='steelblue',
            line=dict(color='black', width=1)
        )
    ))

    # Setze das Layout des Diagramms
    fig.update_layout(
        title=f"Punkteverteilung der Vereine in der Saison {selected_year}",
        xaxis_title="Punktzahl",
        yaxis_title="Verein",
        barmode='group',
        margin={'l': 100, 'r': 100, 't': 50, 'b': 50}
    )

    # Aktualisiere das Balkendiagramm automatisch mit einer Animation
    selected_year += 1
    if selected_year > df['Saison'].max():
        selected_year = df['Saison'].min()

    # Zeige das Diagramm für eine kurze Zeit an
    app.renderer.plotlyjs.serve_figures(fig)

    # Warte für eine Sekunde
    time.sleep(1)

    # Aktualisiere die Seite und rufe die update_bar_chart-Funktion erneut auf
    app.callback_map.clear()
    return update_bar_chart(selected_year)


# Starte die Dash-Anwendung
if __name__ == '__main__':
    app.run_server(debug=True)
