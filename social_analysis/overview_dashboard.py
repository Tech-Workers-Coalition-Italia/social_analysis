import plotly.express as px
from dash import html, dcc

from social_analysis.controls import get_histnorm_from_measure_type
from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_hour_of_day_df, interactions_df


def age_callback(measure_type='Valore Assoluto'):
    histnorm = get_histnorm_from_measure_type(measure_type)
    age_fig = px.histogram(clean_df, x="age", color_discrete_sequence=['wheat'], histnorm=histnorm)
    age_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    return age_fig


def location_callback(measure_type='Valore Assoluto'):
    histnorm = get_histnorm_from_measure_type(measure_type)
    location_fig = px.histogram(clean_df, x="location", color_discrete_sequence=['violet'], histnorm=histnorm)
    location_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    return location_fig


def get_demo_dash():
    return [html.H3(children='Demografia'),
            html.Div([
                dcc.Graph(
                    id='ages',
                ),

                dcc.Graph(
                    id='contract',
                ),
                dcc.Graph(
                    id='location',
                ),

            ], style={'display': 'flex', 'flex-direction': 'row'}),
            ]


def get_habits_dash():
    return [
        html.H3(children='Utilizzo'),

        html.Div(
            [
                dcc.Graph(
                    id='total_time'
                ),
                dcc.Graph(
                    id='hour_of_day'
                ),
                dcc.Graph(
                    id='interactions'
                ),
            ], style={'display': 'flex', 'flex-direction': 'row'})

    ]


def get_overview_dashboards():
    return [html.Div([
        html.H2(children='Overview'),
        *get_demo_dash(),
        html.Hr(),
        *get_habits_dash(),

    ])]
