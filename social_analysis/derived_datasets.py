from social_analysis import df
from social_analysis.dataset_cleaning import clean_df


def exploded_used_social(df):
    df["used_social"]=df["used_social"].apply(lambda x:[p.strip() for p in x.split(";")])
    df=df.explode("used_social")
    return df

exploded_df=exploded_used_social(clean_df)