import plotly.express as px
from dash import html, dcc

from social_analysis.colors import platform_to_colors
from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_communities_df, exploded_used_social_df


def pick_df_by_options(df, follower_type, hour_of_day_select):
    if follower_type == "Follower":
        df = df[df["already_follow"] == True]
    elif follower_type == "Non Follower":
        df = df[df["already_follow"] == False]
    if hour_of_day_select != "Tutti":
        df = df[df[hour_of_day_select.lower()]]

    return df


def make_figure(df_to_use, column, ):
    fig = px.histogram(df_to_use, x=column,
                       color=column, barmode='stack', histfunc="sum",
                       color_discrete_map={**platform_to_colors,
                                           "nessuna": "black"}
                       )

    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'}, )
    return fig


def communities_callback(follower_type, hour_of_day_select):
    exploded_communities_df["communities"] = exploded_communities_df["communities"].replace(
        'no, non sono attivo/a in nessuna comunità online', "nessuna")

    df_to_use = pick_df_by_options(exploded_communities_df, follower_type, hour_of_day_select)
    return make_figure(df_to_use, "communities", )


def platforms_callback(follower_type, hour_of_day_select):
    df_to_use = pick_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    return make_figure(df_to_use, "used_social", )


def platforms_per_job_callback(follower_type, hour_of_day_select):
    df_to_use = pick_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    return px.histogram(df_to_use, x="job", color="used_social",
                        barmode='relative', histfunc="sum",
                        color_discrete_map=platform_to_colors)


def platforms_by_age_callback(follower_type, hour_of_day_select):
    df_to_use = pick_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    return px.histogram(df_to_use, x="age", color="used_social",
                        barmode='relative', histfunc="sum",
                        color_discrete_map=platform_to_colors)


def age_by_platform_callback(follower_type, hour_of_day_select):
    df_to_use = pick_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    return px.histogram(df_to_use, x="used_social", color="age",
                        barmode='relative', histfunc="sum",
                        color_discrete_map=platform_to_colors)


def contact_callback(follower_type, hour_of_day_select):
    df_to_use = pick_df_by_options(clean_df, follower_type, hour_of_day_select)
    return make_figure(df_to_use, "contact_platform", )


def get_platform_dashboards():
    return [html.Div(
        className="row", children=[

            html.H2(children='Piattaforme'),
            dcc.RadioItems(
                ["Tutti", 'Follower', 'Non Follower'],
                value="Tutti",
                id='follower_type',
                inline=True
            ), dcc.RadioItems(
                ["Tutti", "Mattina", 'Pausa Pranzo', 'Pomeriggio', 'Sera', ],
                value="Tutti",
                id='hour_of_day_select',
                inline=True
            ),
            html.Div(
                className="five columns", children=[
                    html.H3(children='Piattaforma su cui hanno trovato il survey'),
                    dcc.Graph(
                        id='contact',
                    ),
                    html.H3(children='Adozione Piattaforme'),

                    dcc.Graph(
                        id='platforms',
                    ),
                ]),
            html.Div(
                className="five columns", children=[
                    html.H3(children='Comunità'),

                    dcc.Graph(
                        id='communities',
                    ),

                    html.H3(children='Piattaforma divisa per lavoro'),
                    dcc.Graph(
                        id='platform_per_job',
                    ),
                ]
            ),
            html.Div(
                className="five columns", children=[

                    html.H3(children='Piattaforma per età'),

                    dcc.Graph(
                        id='platforms_by_age',
                    ),
                    html.H3(children='Distribuzione età per piattaforma'),

                    dcc.Graph(
                        id='age_by_platform',
                    ),
                ]
            ),

        ]),
    ]
