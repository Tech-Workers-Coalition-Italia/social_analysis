from dash import Dash, html, Output, Input

from overview_dashboard import contract_callback
from social_analysis.evening_dashboard import get_evening_dashboard
from social_analysis.overview_dashboard import get_overview_dashboards
from social_analysis.platform_dashboard import communities_callback, platforms_callback, get_platform_dashboards, \
    platforms_per_job_callback, contact_callback, platforms_by_age_callback, age_by_platform_callback

app = Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='Presentazione Social Survey'),

    *get_overview_dashboards(),

    html.Hr(),
    *get_platform_dashboards(),
    *get_evening_dashboard()

])

app.callback(
    Output('ages', 'figure'),
    Input('measure_type', 'value'),
)(contract_callback)

app.callback(
    Output('location', 'figure'),
    Input('measure_type', 'value'),
)(contract_callback)

app.callback(
    Output('contract', 'figure'),
    Input('measure_type', 'value'),
)(contract_callback)

callback_input=[
    Input('follower_type', 'value'),
    Input('hour_of_day_select', 'value'),
]
app.callback(
    Output('platforms', 'figure'),
    *callback_input,

)(platforms_callback)

app.callback(
    Output('communities', 'figure'),
    *callback_input,
)(communities_callback)

app.callback(
    Output('platform_per_job', 'figure'),
    *callback_input,
)(platforms_per_job_callback)

app.callback(
    Output('contact', 'figure'),
    *callback_input,
)(contact_callback)

app.callback(
    Output('platforms_by_age', 'figure'),
    *callback_input,
)(platforms_by_age_callback)

app.callback(
    Output('age_by_platform', 'figure'),
    *callback_input,
)(age_by_platform_callback)

server=app.server

if __name__ == '__main__':
    app.run_server(debug=True)