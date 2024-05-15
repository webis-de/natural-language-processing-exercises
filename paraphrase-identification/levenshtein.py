import nltk
import pandas as pd


def levenshtein_distance(df: pd.DataFrame):
    text = df.map(nltk.word_tokenize)
    distance = text.apply(lambda x: nltk.edit_distance(x.iloc[0], x.iloc[1]), axis=1)
    return distance
