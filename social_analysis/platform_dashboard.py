import plotly.express as px
from dash import html, dcc

from social_analysis.colors import platform_to_colors
from social_analysis.controls import get_histnorm_from_measure_type
from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_communities_df, exploded_used_social_df, exploded_hour_of_day_df, \
    interactions_df


def pick_platform_df_by_options(df, follower_type, hour_of_day_select):
    if follower_type == "Follower":
        df = df[df["already_follow"] == True]
    elif follower_type == "Non Follower":
        df = df[df["already_follow"] == False]
    if hour_of_day_select != "Tutti":
        df = df[df[hour_of_day_select.lower()]]

    return df


def total_time_callback(measure_type):
    histnorm = get_histnorm_from_measure_type(measure_type)
    total_time_fig = px.histogram(clean_df, x="total_time",
                                  category_orders={"total_time": [
                                      "meno di 1 ora",
                                      "da 1 a 2 ore",
                                      "da 2 a 3 ore",
                                      "più di 3 ore"]
                                  },
                                  color_discrete_sequence=['green'], histnorm=histnorm
                                  )
    return total_time_fig


def hour_of_day_callback(measure_type):
    histnorm = get_histnorm_from_measure_type(measure_type)
    hour_of_day_fig = px.histogram(exploded_hour_of_day_df, x="hour_of_day",
                                   histfunc="sum",
                                   category_orders={"hour_of_day": [
                                       "mattina",
                                       "pausa pranzo",
                                       "pomeriggio",
                                       "sera"]
                                   },
                                   color_discrete_sequence=['indianred'], histnorm=histnorm
                                   )
    return hour_of_day_fig


def interactions_callback(measure_type):
    histnorm = get_histnorm_from_measure_type(measure_type)
    interactions_fig = px.histogram(interactions_df, x="interactions",
                                    histfunc="sum",
                                    color_discrete_sequence=['turquoise'], histnorm=histnorm
                                    )
    return interactions_fig


def contract_callback(measure_type):
    histnorm = get_histnorm_from_measure_type(measure_type)
    contract_fig = px.histogram(clean_df, x="contract", color_discrete_sequence=['pink'], histnorm=histnorm)
    contract_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'}, )
    return contract_fig




def make_figure(df_to_use, column ):
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

    df_to_use = pick_platform_df_by_options(exploded_communities_df, follower_type, hour_of_day_select)
    return make_figure(df_to_use, "communities", )


def platforms_callback(follower_type, hour_of_day_select):
    df_to_use = pick_platform_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    return make_figure(df_to_use, "used_social", )


def platforms_per_job_callback(follower_type, hour_of_day_select):
    df_to_use = pick_platform_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    return px.histogram(df_to_use, x="job", color="used_social",
                        barmode='relative', histfunc="sum",
                        color_discrete_map=platform_to_colors)


def platforms_by_age_callback(follower_type, hour_of_day_select):
    df_to_use = pick_platform_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    return px.histogram(df_to_use, x="age", color="used_social",
                        barmode='relative', histfunc="sum",
                        color_discrete_map=platform_to_colors)


def age_by_platform_callback(follower_type, hour_of_day_select,measure_type):

    df_to_use = pick_platform_df_by_options(exploded_used_social_df, follower_type, hour_of_day_select)
    if measure_type == "Valore Assoluto":
        return px.histogram(df_to_use, x="used_social", color="age",
                            barmode='relative', histfunc="sum",
                            color_discrete_map=platform_to_colors)
    else:
        counts=df_to_use.groupby(["age","used_social"]).size()
        counts=counts.groupby(["used_social"]).apply(lambda x:x/x.sum())
        counts=counts.reset_index(level=["used_social","age"])
        return px.bar(counts, x="used_social", y=0,color="age",
                            color_discrete_map=platform_to_colors)


def contact_callback(follower_type, hour_of_day_select):
    df_to_use = pick_platform_df_by_options(clean_df, follower_type, hour_of_day_select)
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
