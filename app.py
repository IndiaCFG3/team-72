from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
stopwords = stopwords.words('english')


import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import io


app = Flask(__name__)
CORS(app, support_credentials=True)

def pre_process(text):
    """

    :param text: Unprocessed text
    :return: Processed text
    """
    text = text.lower()
    text = re.sub('&lt;/?.*?&gt', '&lt;&gt', text)
    text = re.sub("(\\d|\\W)+", " ", text)
    return text

def sort_coo(coo_matrix):
    """

    :param coo_matrix: COO Matrix
    :return: Sorted matrix based on data in descending order
    """
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """

    :param feature_names: Feature names of keywords from word count vector
    :param sorted_items: Matrix from sort_coo matrix
    :param topn: Number of keywords required
    :return: Dictionary with words as keys and score as values
    """
    sorted_items = sorted_items[:topn]
    score_vals, feature_vals = [], []
    for idx, score in sorted_items:
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]
    return results


def plot_stacked_bar_chart(x_attributes, y_values, ind_labels, x_label, title):
    """ renders the plot on the fly.
    """
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    N = len(x_attributes)
    ind = np.arange(N)
    width = 0.3
    for i in range(len(y_values)):
        ax.bar(ind+width*i, y_values[i], width)
    ax.set_xlabel(x_label)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(tuple(x_attributes))
    ax.set_yticks(np.arange(0,101,10))
    ax.set_title(title)

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return output


@app.route('/')
def hello_world():
    # Sandbox testing
    skills = [['hi', 'hello', 'hey','heya'], ['hi', 'hello', 'hey','heya']]
    y_pos = [[10,20,30,50], [20,40,60,80]]
    atts = ['jan', 'feb']
    df = pd.DataFrame({})
    output = plot_stacked_bar_chart(atts, y_pos, skills, 'Performance', 'Fast')
    return Response(output.getvalue(), mimetype="image/png")


@app.route('/comments/keywords', methods=['POST'])
def extract_keywords():
    data = request.json
    #print(data)
    text_values = [eval(z) for z in list(data.values())]
    #print(text_values)
    attribute_values = list(data.keys())
    res = {}
    for i in range(len(text_values)):
        text_values[i] = [pre_process(z) for z in text_values[i]]
        #print(text_values[i])
        cv = CountVectorizer(max_df=0.85, stop_words=stopwords, max_features=10000)
        word_count_vector = cv.fit_transform(text_values[i])
        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        tfidf_transformer.fit(word_count_vector)
        feature_names = cv.get_feature_names()
        doc = ''.join(d for d in text_values[i])
        tf_idf_vector = tfidf_transformer.fit_transform(cv.transform([doc]))
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        keywords={}
        keywords = extract_topn_from_vector(feature_names, sorted_items)
        #print(keywords)
        res[attribute_values[i]] = keywords
    return res


@app.route('/comments/sentiment', methods=['POST'])
def decide_which_product_kit():
    data = request.json
    points = eval(data['points'])
    data.pop('points')
    text_values = [eval(z) for z in list(data.values())]
    attribute_values = list(data.keys())
    assert len(attribute_values) == len(points.keys())  # Sanity check
    res = {}
    analyser = SentimentIntensityAnalyzer()
    for i in range(len(text_values)):
        text_values[i] = '.'.join(t for t in text_values[i])
        score = analyser.polarity_scores(text_values[i])
        res[attribute_values[i]] = score['compound']

    for z in list(points.keys()):
        res[z] += points[z]

    return res  # Recommend the one with the lowest score


if __name__ == '__main__':
    app.run()
