import plotly.express as px
from dash import html, dcc

from social_analysis.dataset_cleaning import clean_df
from social_analysis.derived_datasets import exploded_hour_of_day_df, interactions_df


def age_callback(measure_type='Valore Assoluto'):
    assert measure_type in ('Valore Assoluto', 'Valore Relativo'), f"Invalid measure_type value {measure_type}"
    histnorm = "probability" if measure_type == 'Valore Relativo' else None
    age_fig = px.histogram(clean_df, x="age", color_discrete_sequence=['wheat'], histnorm=histnorm)
    age_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    return age_fig


def location_callback(measure_type='Valore Assoluto'):
    assert measure_type in ('Valore Assoluto', 'Valore Relativo'), f"Invalid measure_type value {measure_type}"
    histnorm = "probability" if measure_type == 'Valore Relativo' else None
    location_fig = px.histogram(clean_df, x="location", color_discrete_sequence=['violet'], histnorm=histnorm)
    location_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    return location_fig


def contract_callback(measure_type='Valore Assoluto'):
    assert measure_type in ('Valore Assoluto', 'Valore Relativo'), f"Invalid measure_type value {measure_type}"
    histnorm = "probability" if measure_type == 'Valore Relativo' else None
    contract_fig = px.histogram(clean_df, x="contract", color_discrete_sequence=['pink'], histnorm=histnorm)
    contract_fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'}, )
    return contract_fig


def get_demo_dash(prefix=""):
    return [html.H3(children='Demografia'),
            dcc.RadioItems(
                ['Valore Assoluto', 'Valore Relativo'],
                'Valore Assoluto',
                id='measure_type',
                inline=True,
            ),
            html.Div([
                dcc.Graph(
                    id=prefix + 'ages',
                ),

                dcc.Graph(
                    id=prefix + 'location',
                ),

                dcc.Graph(
                    id=prefix + 'contract',
                ),
            ], style={'display': 'flex', 'flex-direction': 'row'}),
            ]


def get_habits_dash():
    total_time_fig = px.histogram(clean_df, x="total_time",
                                  category_orders={"total_time": [
                                      "meno di 1 ora",
                                      "da 1 a 2 ore",
                                      "da 2 a 3 ore",
                                      "più di 3 ore"]
                                  }, color_discrete_sequence=['green']
                                  )

    hour_of_day_fig = px.histogram(exploded_hour_of_day_df, x="hour_of_day",
                                   histfunc="sum",
                                   category_orders={"hour_of_day": [
                                       "mattina",
                                       "pausa pranzo",
                                       "pomeriggio",
                                       "sera"]
                                   }, color_discrete_sequence=['indianred']
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


def get_overview_dashboards():
    return [html.Div([
        html.H2(children='Overview'),
        *get_demo_dash(),
        html.Hr(),
        *get_habits_dash(),

    ])]
