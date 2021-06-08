#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def Review_Classification(df):

    classifer_model = pickle.load(open('Classification/Trained_Classifier_model.sav', 'rb'))

    df = df.drop(['Customer ID'], axis=1)
    df = df.drop(['Customer Name'], axis=1)
    df = df.drop(['Review Titles'], axis=1)
    df = df.drop(['Review Body'], axis=1)
    df = df.drop(['Review Date'], axis=1)
    df = df.drop(['Helpful Votes'], axis=1)

    le = LabelEncoder()
    df['Encoded Product Name'] = le.fit_transform(df['Product Name'])
    df = df.drop(['Product Name'], axis=1)

    result = classifer_model.predict(df)

    df['Fake/Real'] = result

    return df

if __name__ == "__main__":
    Review_Classification(df)





