from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import sys

from social_analysis.dataset_cleaning import clean_dataset
from social_analysis.derived_datasets import exploded_used_social

app = Dash(__name__)

df = pd.read_csv(sys.argv[1])
df = clean_dataset(df)



fig = px.histogram(exploded_used_social(df),x="job",color="used_social",barmode='stack',histfunc="sum")
app.layout = html.Div(children=[
    html.H1(children='Presentazione Social Survey'),

    html.H2(children="Adozione piattaforme per lavoro"),

    dcc.Graph(
        id='platform_per_job',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)