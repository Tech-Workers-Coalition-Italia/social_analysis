from social_analysis import df
from social_analysis.dataset_cleaning import clean_df


def splitter(x):
    if type(x) is float:
        return []
    return [p.strip() for p in x.split(";")]


def exploded_used_social(df):
    df["used_social"] = df["used_social"].apply(splitter)
    df = df.explode("used_social")

    return df

def exploded_hour_of_day(df):
    df["hour_of_day"] = df["hour_of_day"].apply(splitter)
    return df.explode("hour_of_day")

def interactions(df):
    df["interactions"] = df["interactions"].apply(splitter)
    return df.explode("interactions")

def exploded_communities(df):
    df["communities"] = df["communities"].apply(splitter)
    return df.explode("communities")


exploded_used_social_df = exploded_used_social(clean_df)
exploded_hour_of_day_df = exploded_hour_of_day(clean_df)
interactions_df = interactions(clean_df)
exploded_communities_df = exploded_communities(clean_df)