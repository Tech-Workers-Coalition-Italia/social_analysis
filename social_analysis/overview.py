import plotly.express as px
from dash import html, dcc

from social_analysis.derived_datasets import exploded_df


def get_overview_dash():
    return [    html.H2(children='Overview'),
                dcc.RadioItems(
                    ['Follower', 'Non Follower'],
                    value="Follower",
                    id='follower_type',
                    inline=True
                ),
                dcc.Graph(
                    id='platforms',
                ),
                ]

def follower_type_callback(follower_type):
    is_follower=follower_type=="Follower"
    platforms_fig=px.histogram(exploded_df[exploded_df["already_follow"] == is_follower], x="used_social", color="used_social", barmode='stack', histfunc="sum")

    return platforms_fig