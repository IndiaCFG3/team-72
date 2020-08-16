from flask import Flask, request, Response, send_file
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import re
import os
import waterfall_chart
import matplotlib

matplotlib.use('Agg')
import nltk

nltk.download("stopwords")
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


@app.route('/')
def hi():
    return 'hello world'


@app.route('/test')
def hello_world():
    # Sandbox testing
    skills = [['hi', 'hello', 'hey', 'heya'], ['hi', 'hello', 'hey', 'heya']]
    y_pos = [[10, 20, 30, 50], [20, 40, 60, 80]]
    atts = ['jan', 'feb']
    df = pd.DataFrame({})
    output = plot_stacked_bar_chart(atts, y_pos, skills, 'Performance', 'Fast')
    return Response(output.getvalue(), mimetype="image/png")


@app.route('/student/<performance_type>', methods=['POST'])
def create_bar_graph(performance_type):
    """

    :param performance_type: self : students own performance
    :return: path to stored bar chart for given months and skill
    """
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    data = request.json
    skills = request.form.get('skills')
    skills = eval(skills)
    values = request.form.get('values')
    values = eval(values)
    print(values)
    months = request.form.get('months')
    months = eval(months)
    N = len(skills)
    x = np.arange(N)
    p = []
    for i in range(N):
        p.append(ax.bar(x + i * 0.25, values[i], width=0.25))
    z = [*p]
    ax.legend(handles=z , labels=skills, loc='upper left')
    ax.figure.savefig('image.png')
    return {'path': f'{os.getcwd()}/image.png'}


@app.route('/comments/keywords', methods=['POST'])
def extract_keywords():
    skills = request.form.get('skills')
    values = request.form.get('comments')
    attribute_values = eval(skills)
    values = eval(values)
    res = {}
    for i in range(len(values)):
        values[i] = [pre_process(z) for z in values[i]]
        # print(text_values[i])
        cv = CountVectorizer(max_df=0.85, stop_words=stopwords, max_features=10000)
        word_count_vector = cv.fit_transform(values[i])
        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        tfidf_transformer.fit(word_count_vector)
        feature_names = cv.get_feature_names()
        doc = ''.join(d for d in values[i])
        tf_idf_vector = tfidf_transformer.fit_transform(cv.transform([doc]))
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        keywords = {}
        keywords = extract_topn_from_vector(feature_names, sorted_items)
        # print(keywords)
        res[attribute_values[i]] = keywords
    return res


@app.route('/comments/sentiment', methods=['POST'])
def decide_which_product_kit():
    skills = request.form.get('skills')
    values = request.form.get('comments')
    points = request.form.get('points')
    points = eval(points)
    attribute_values = eval(skills)
    text_values = eval(values)
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


@app.route('/class/perform', methods=['POST'])
def send_waterfall_chart():
    data = {'skill': request.form.get('skill'),
            'values': request.form.get('values'),
            'months': request.form.get('months')}
    print(data)
    data['months'] = eval(data['months'])
    data['values'] = eval(data['values'])
    data['values'] = [float(x) for x in data['values']]
    for i in range(1, len(data['values'])):
        data['values'][i] -= data['values'][i - 1]
    waterfall_chart.plot(data['months'], data['values'], Title=data['skill']).savefig(
        f'{data["skill"]}{len(data["months"])}.png')
    return {'Path': f"{os.getcwd()}/{data['skill']}{len(data['months'])}.png"}


if __name__ == '__main__':
    app.run()
