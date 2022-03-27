import plotly.express as px
from dash import html, dcc

from social_analysis.colors import platform_to_colors
from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_communities_df, exploded_used_social_df
from social_analysis.overview import get_demo_dash


def filter_evening(df):
    return df[df["sera"]]



def get_evening_dashboard():

    return [html.Div(
        className="row", children=[

            html.H2(children='Sera'),
            *get_demo_dash(filter_evening(clean_df), prefix="evening_")
        ])

    ]
