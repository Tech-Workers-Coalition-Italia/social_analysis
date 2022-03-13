import plotly.express as px
from dash import html, dcc

from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_df


def get_demo_dash():
    age_fig = px.histogram(clean_df, x="age")
    age_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})

    location_fig = px.histogram(clean_df, x="location", )
    location_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

    contract_fig = px.histogram(clean_df, x="contract", )
    contract_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

    return [html.H3(children='Demografia'),
            html.Div([
                dcc.Graph(
                    id='ages',
                    figure=age_fig
                ),

                dcc.Graph(
                    id='location',
                    figure=location_fig),

                dcc.Graph(
                    id='contract',
                    figure=contract_fig),
            ], style={'display': 'flex', 'flex-direction': 'row'}),
            ]


def get_overview_dash():
    return [html.Div([
        html.H2(children='Overview'),
        *get_demo_dash(),

        html.H3(children='Adozione Piattaforme'),
        dcc.RadioItems(
            ['Follower', 'Non Follower'],
            value="Follower",
            id='follower_type',
            inline=True
        ),
        dcc.Graph(
            id='platforms',
        )]),
    ]


def follower_type_callback(follower_type):
    is_follower = follower_type == "Follower"
    platforms_fig = px.histogram(exploded_df[exploded_df["already_follow"] == is_follower], x="used_social",
                                 color="used_social", barmode='stack', histfunc="sum")

    return platforms_fig
