def exploded_used_social(df):
    df["used_social"]=df["used_social"].apply(lambda x:[p.strip() for p in x.split(";")])
    df=df.explode("used_social")
    return df