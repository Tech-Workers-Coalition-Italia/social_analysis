import numpy as np
import pandas as pd

PLATFORM_LIST=[
    "Facebook",
    "Linkedin",
    "Instagram",
    "Youtube",
    "Reddit",
    "Telegram",
    "Discord",
    "Twitter",
    "Mastodon",
    "altro",
    "Matrix",

]
def clean_dataset(df):
    df=rename_fields(df)
    df=fill_missing(df)
    df=map_string_values(df)
    df=unpack_multiple_answers(df)
    return df

def rename_fields(df):
    df=df.rename(columns={
        "Di cosa ti occupi?":"job",
        "Marca temporale":"datetime",
        "Quanti anni hai?":"age",
        "Come sei venuto in contatto con questo questionario?":"contact_platform",
        "Segui già Tech Workers Coalition Italia su almeno una piattaforma social?":"already_follow",
        "Quali social network utilizzi almeno una volta al giorno?":"used_social",
        "Quante ore al giorno utilizzi i social?":"hours_used",
        "Che tipo di rapporto lavorativo hai?":"contract",
        "Dove vivi?":"location",
        "Come interagisci sui social?":"interactions",
        "Se sei attivo/a in una o più comunità online, su quale/i social network si trovano?":"communities",
        "Se hai selezionato \"altro\" all'ultima domanda, puoi specificare qui la piattaforma che volevi inserire:":"other_platforms"
    })
    return df

def fill_missing(df):
    """some questions have been added while the survey was already launched.
    We know what the correct answer for the people that already compiled the survey are, so we fill the gaps
    """

    # when the question was added, the survey was only on telegram
    df["contact_platform"]=df["contact_platform"].fillna("Telegram")


    # when the question was added, the survey was only on TWC channels
    df["already_follow"]=df["already_follow"].fillna("Sì")
    return df

def map_string_values(df):
    df=df.replace("Sì",True)
    df=df.replace("No",False)

    df=df.replace("da 31 a 45","31-45")
    df=df.replace("da 21 a 30","21-30")
    df=df.replace("più di 45","45+")
    df=df.replace("meno di 21","21-")

    return df

def unpack_multiple_answers(df):

    df=df.join(df.communities.str.get_dummies(sep=";").astype(bool),lsuffix="uses_",rsuffix="_daily")
    df=df.join(df.used_social.str.get_dummies(sep=";").astype(bool),lsuffix="in_", rsuffix="_community")

    return df
