import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'venv/Lib/site-packages')))

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import sklearn.datasets
import pandas as pd
from sklearn.pipeline import Pipeline

# returns (model, count_vect, tfidf, error), where model is the model you use to predict
def fit_model(filepath):
    # fill in the filepath
    df = pd.read_csv(filepath)
    df.columns = ['ticker', 'string', 'upvotes', 'target']

    # take the top half of the upvotes
    df = df[df['upvotes'] > df['upvotes'].quantile(.5)]

    df_train = df.sample(frac = .8)
    df_test = df.sample(frac = .2)

    # set posts and target from train
    posts_train = df_train['string']
    target_train = df_train['target']
    
    meme_train = sklearn.datasets.base.Bunch(data = posts_train, 
                                      target = target_train)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(meme_train.data)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, meme_train.target)
    
    # find how good it is on test data
    X_test_counts = count_vect.transform(df_test['string'])
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    predicted = clf.predict(X_test_tfidf)
    testError = df_test['target'] != predicted
    resErr = (len(df_test['target']) - 
              np.sum(testError))/len(df_test['target'])
    return (clf, count_vect, tfidf_transformer, resErr)


# input: model, count_vect, tfidf, and list of posts
# output: predictions
def predict_price(model, count_vect, tfidf, posts):
    post_counts = count_vect.transform(posts)
    post_tfidf = tfidf.transform(post_counts)
    return model.predict(post_tfidf)

postreqdata = json.loads(open(os.environ['req']).read())
redditPosts = postreqdata['redditPosts']

(model, count_vect, tfidf, error) = fit_model("data.csv")
predictions = predict_price(model, count_vect, tfidf, redditPosts)

response = open(os.environ['res'], 'w')
response.write(json.dumps(predictions.tolist()))
response.close()