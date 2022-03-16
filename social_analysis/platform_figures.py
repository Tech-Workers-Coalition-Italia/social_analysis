from plotly import express as px

from social_analysis.colors import platform_to_colors
from social_analysis.derived_datasets import exploded_communities_df, exploded_used_social_df


def pick_df_by_options(df,follower_type):
    if follower_type == "Follower":
        df= df[df["already_follow"] == True]
    elif follower_type == "Non Follower":
        df= df[df["already_follow"] == False]

    return df


def make_figure(df_to_use, column, social_count_type):

    if social_count_type=='Pesata per social di contatto':
        pass

    else:
        fig= px.histogram(df_to_use, x=column,
                 color=column, barmode='stack', histfunc="sum",
                          color_discrete_map={**platform_to_colors,
                                              "no, non sono attivo/a in nessuna comunità online":"black"}
                          )

    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'},)
    return fig

def communities_callback(follower_type, social_count_type):

    df_to_use=pick_df_by_options(exploded_communities_df,follower_type)
    return make_figure(df_to_use,"communities",social_count_type)


def platforms_callback(follower_type, social_count_type):
    df_to_use=pick_df_by_options(exploded_used_social_df,follower_type)
    return make_figure(df_to_use,"used_social",social_count_type)