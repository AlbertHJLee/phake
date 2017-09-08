"""
Tools for analyzing article data
"""

import os
import sys
import json
import pandas
import sklearn

from sklearn.feature_extraction.text import CountVectorizer



def loadData():

    with open('data/posts.json','r') as infile:
        posts = json.load(infile)

    with open('data/pages.json','r') as infile:
        pages = json.load(infile)

    return pages, posts




def get_bagofwords():

    """
    Get simple vectorized bag of words
    """

    [pages,posts] = loadData()

    vectorizer = CountVectorizer()
    corpus = []
    sources = []
    
    for post in posts:

        sources += [post[u'from'][u'name']]
        if u'message' in post:
            corpus += [post[u'message']]
        elif u'description' in post:
            corpus += [post[u'description']]
        else:
            corpus += ['']

    tokens = vectorizer.fit_transform(corpus)

    return tokens, vectorizer, sources, corpus




def numpy2pandas(tokens,sources):

    data = pandas.DataFrame(x,index=sources)

    return data




def frequentWords(data):

    totals = data.sum()
    peaks = totals > 100
    
    bySource = data.ix['Fox 8 News',peaks].sum()
    bySource = data.ix['ABC News',peaks].sum()

    return True

