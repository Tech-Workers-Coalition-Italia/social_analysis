from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import sys

from social_analysis.dataset_cleaning import clean_dataset

app = Dash(__name__)

df = pd.read_csv(sys.argv[1])
df = clean_dataset(df)
fig = px.histogram(df,x="job",y="already_follow")
app.layout = html.Div(children=[
    html.H1(children='Presentazione Social Survey'),


    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)