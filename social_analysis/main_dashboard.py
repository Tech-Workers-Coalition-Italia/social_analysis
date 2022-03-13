import plotly.express as px
from dash import Dash, html, dcc, Output, Input

from social_analysis.derived_datasets import exploded_used_social_df
from social_analysis.overview import get_overview_dash, follower_type_callback

app = Dash(__name__)

platforms_per_job_fig = px.histogram(exploded_used_social_df, x="job", color="used_social", barmode='stack', histfunc="sum")

app.layout = html.Div(children=[
    html.H1(children='Presentazione Social Survey'),

    *get_overview_dash(),
    html.H3(children="Adozione piattaforme per lavoro"),

    dcc.Graph(
        id='platform_per_job',
        figure=platforms_per_job_fig
    )
])

app.callback(
    Output('platforms', 'figure'),
    Input('follower_type', 'value'),)(follower_type_callback)

if __name__ == '__main__':
    app.run_server(debug=True)