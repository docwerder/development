import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from tabulate import tabulate
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
df_eternal = pd.read_csv(r"/Users/joerg/repos/development/blMeister_all_years.csv")

# Erstelle eine leere Liste, um die Ergebnisse zu speichern
result_list = []
# Wähle eine bestimmte Zeile aus dem Dataframe
selected_row = df_eternal.loc[0] 
# print(f"selected_row: {selected_row}")
# Iteriere über jede Zeile des Dataframes
for index, row in df_eternal.iloc[1:2].iterrows():
    # Iteriere über jeden Verein in der aktuellen Zeile
    for column in df_eternal.columns:
        # Füge den Vereinsnamen und die Punktzahl zur Ergebnisliste hinzu
        result_list.append(column)
        result_list.append(row[column])

# print(result_list)
# Definiere eine Funktion, um die Punkte eines Vereins aus der Liste abzurufen
def get_points(item):
    if item == 'Saison':
        return -1
    elif isinstance(item, int):
        return item
    else:
        return 0
    
# Sortiere die Liste nach den Punkten der Vereine
sorted_data = sorted(result_list, key=get_points, reverse=True)
print(sorted_data)

# Extrahiere das Jahr aus der Liste
year = sorted_data[0]

# Extrahiere die Vereinsnamen und Punkte aus der Liste
teams = sorted_data[1::2]
points = sorted_data[2::2]
print(points)
# Erstelle das horizontale Balkendiagramm
fig = go.Figure(data=go.Bar(
    y=teams,
    x=points,
    orientation='h'
))



# Setze das Layout des Diagramms
fig.update_layout(
    title=f"Balkendiagramm für das Jahr {year}",
    xaxis_title="Verein",
    yaxis_title="Punktezahl",
    barmode='group'
)

# Zeige das Diagramm an
fig.show()
