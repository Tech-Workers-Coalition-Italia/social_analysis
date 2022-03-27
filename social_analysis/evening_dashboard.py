import plotly.express as px
from dash import html, dcc

from social_analysis.colors import platform_to_colors
from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_communities_df, exploded_used_social_df
from social_analysis.overview import get_demo_dash
from plotly import graph_objs as go


def filter_evening(df):
    return df[df["sera"]]


def filter_not_evening(df):
    return df[~df["sera"]]


def make_evening_comparison(evening_df, not_evening_df, column):
    fig = go.Figure()
    all_counts = clean_df[column].value_counts()
    evening_count = evening_df[column].value_counts()
    not_evening_count = not_evening_df[column].value_counts()
    evening_count = evening_count / all_counts
    not_evening_count = not_evening_count / all_counts

    fig.add_trace(go.Bar(x=evening_count.keys(), y=evening_count,
                         name='Sera'))
    fig.add_trace(go.Bar(x=not_evening_count.keys(), y=not_evening_count,
                         name='Altri'
                         ))

    fig.update_layout(xaxis={'categoryorder': 'category ascending'})
    return fig


def get_evening_dashboard():
    evening_df = filter_evening(clean_df)
    not_evening_df = filter_not_evening(clean_df)
    age_fig = make_evening_comparison(evening_df, not_evening_df, "age")
    location_fig = make_evening_comparison(evening_df, not_evening_df, "location")
    job_fig = make_evening_comparison(evening_df, not_evening_df, "job")
    return [
        html.H3(children='Sera'),
        html.H3(
            children='I valori sono percentuali del totale per una data categoria. Va migliorata la visualizzazione'),
        html.Div([
            dcc.Graph(
                id='evening_ages',
                figure=age_fig,
            ), dcc.Graph(
                id='evening_location',
                figure=location_fig,
            ),
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        html.Div([
            dcc.Graph(
                id='evening_job',
                figure=job_fig,
            ),
        ], style={'display': 'flex', 'flex-direction': 'row'}),

    ]
