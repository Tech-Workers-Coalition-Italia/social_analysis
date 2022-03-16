import plotly.express as px
from dash import Dash, html, dcc, Output, Input

from social_analysis.colors import platform_to_colors
from social_analysis.derived_datasets import exploded_used_social_df
from social_analysis.overview import get_overview_dash
from social_analysis.platform_dashboard import communities_callback, platforms_callback, get_platform_dashboards, \
    platforms_per_job_callback

app = Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='Presentazione Social Survey'),

    *get_overview_dash(),

    html.Hr(),
    *get_platform_dashboards(),

])

app.callback(
    Output('platforms', 'figure'),
    Input('follower_type', 'value'),
    Input('social_count_type', 'value'),
)(platforms_callback)

app.callback(
    Output('communities', 'figure'),
    Input('follower_type', 'value'),
    Input('social_count_type', 'value'),
)(communities_callback)

app.callback(
    Output('platform_per_job', 'figure'),
    Input('follower_type', 'value'),
)(platforms_per_job_callback)

server=app.server

if __name__ == '__main__':
    app.run_server(debug=True)