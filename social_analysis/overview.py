import plotly.express as px
from dash import html, dcc

from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_used_social_df, exploded_hour_of_day_df, interactions_df, \
    exploded_communities_df


def get_demo_dash():
    age_fig = px.histogram(clean_df, x="age",color_discrete_sequence=['wheat'])
    age_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})

    location_fig = px.histogram(clean_df, x="location", color_discrete_sequence=['violet'])
    location_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

    contract_fig = px.histogram(clean_df, x="contract",
                                color_discrete_sequence=['pink'])
    contract_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'},)

    return [html.H3(children='Demografia'),
            html.Div([
                dcc.Graph(
                    id='ages',
                    figure=age_fig,
                ),

                dcc.Graph(
                    id='location',
                    figure=location_fig),

                dcc.Graph(
                    id='contract',
                    figure=contract_fig),
            ], style={'display': 'flex', 'flex-direction': 'row'}),
            ]


def get_habits_dash():
    total_time_fig = px.histogram(clean_df, x="total_time",
                                  category_orders={"total_time": [
                                      "meno di 1 ora",
                                      "da 1 a 2 ore",
                                      "da 2 a 3 ore",
                                      "più di 3 ore"]
                                  },color_discrete_sequence=['green']
                                  )

    hour_of_day_fig = px.histogram(exploded_hour_of_day_df, x="hour_of_day",
                                   histfunc="sum",
                                   category_orders={"hour_of_day": [
                                       "mattina",
                                       "pausa pranzo",
                                       "pomeriggio",
                                       "sera"]
                                   },color_discrete_sequence=['indianred']
                                   )

    interactions_fig = px.histogram(interactions_df, x="interactions",
                                   histfunc="sum",
                                   color_discrete_sequence=['turquoise']
                                   )

    return [
        html.H3(children='Utilizzo'),

            html.Div(
                [
                dcc.Graph(
                    id='total_time',
                    figure=total_time_fig
                ),
                    dcc.Graph(
                        id='hour_of_day',
                        figure=hour_of_day_fig
                    ),
                    dcc.Graph(
                        id='interactions',
                        figure=interactions_fig
                    ),
            ], style={'display': 'flex', 'flex-direction': 'row'})

    ]


def get_overview_dash():
    return [html.Div([
        html.H2(children='Overview'),
        *get_demo_dash(),
        html.Hr(),
        *get_habits_dash(),
        html.Hr(),
        html.H3(children='Adozione Piattaforme'),
        dcc.RadioItems(
            ["Tutti",'Follower', 'Non Follower'],
            value="Tutti",
            id='follower_type',
            inline=True
        ),
        dcc.RadioItems(
            ['Totale',
             #'Pesata per social di contatto'
             ],
            value="Totale",
            id='social_count_type',
            inline=True
        ),
        dcc.Graph(
            id='platforms',
        )]),

        html.H3(children='Comunità'),

        dcc.Graph(
            id='communities',
        ),
    ]

def remove_contact(row):
    row["used_social"]=row["used_social"].remove(row["contact_platform"])
    return row

def pick_df_by_options(df,follower_type, social_count_type):
    if follower_type == "Follower":
        df= df[df["already_follow"] == True]
    elif follower_type == "Non Follower":
        df= df[df["already_follow"] == False]


    if social_count_type=='Pesata per social di contatto':
        # not implemented yet
        df = df

    return df

def communities_callback(follower_type, social_count_type):

    df_to_use=pick_df_by_options(exploded_communities_df,follower_type,social_count_type)


    communities_fig = px.histogram(df_to_use, x="communities",
                                 color="communities", barmode='stack', histfunc="sum")

    return communities_fig

def platforms_callback(follower_type, social_count_type):
    df_to_use=pick_df_by_options(exploded_used_social_df,follower_type,social_count_type)


    platforms_fig = px.histogram(df_to_use, x="used_social",
                                 color="used_social", barmode='stack', histfunc="sum")

    return platforms_fig
