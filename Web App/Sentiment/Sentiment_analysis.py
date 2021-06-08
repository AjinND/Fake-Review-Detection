#!/usr/bin/env python
# coding: utf-8

# In[20]:

import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
import numpy as np

def sentiment_analysis2(df):
    loaded_model = pickle.load(open('Sentiment/finalized_model.sav', 'rb'))
    input_list = df['Review Body']
    #print(input_list.shape)
    result = loaded_model.predict(input_list)
    #print(np.unique(result,return_counts=True))

    df['SENTIMENT'] = result
    df["SENTIMENT"].replace({"__label__1": 0, "__label__2": 1}, inplace=True)

    #df.to_csv('Collected_Reviews.csv', index=False)

    return df


def sentiment_analysis(df):
    loaded_model = pickle.load(open('Sentiment/sentiment_analysis_multinomialNB_model.sav', 'rb'))
    #input_list = df['REVIEW_TEXT']
        
    matrix = CountVectorizer(max_features=1000, stop_words="english")
    input_list = matrix.fit_transform(df['Review Body'].values.astype('U')).toarray()
    #print(input_list.shape)

    result = loaded_model.predict(TfidfTransformer().fit_transform(input_list))
    #print(np.unique(result,return_counts=True))
    df['SENTIMENT'] = result

    return df
    #df.to_csv('Collected_Reviews.csv', index=False)

if __name__ == "__main__":
    sentiment_analysis2(df)
    #print(sentiment)
