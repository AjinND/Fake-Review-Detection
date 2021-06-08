from flask import *
import pandas as pd
import matplotlib.pyplot as plt
from Crawler.Data_Collection import *
from Sentiment.Sentiment_analysis import *
from Classification.Fake_Review_Detector import *

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

app = Flask(__name__)  
@app.route('/index')
def my_form():
    return render_template('index.html')

@app.route('/index', methods=['POST', 'GET'])
def index():
    url = request.form['content']
    df = collection(url,headers)

    sentiment_df = sentiment_analysis2(df)

    final_result = Review_Classification(sentiment_df)
    final_result['Fake/Real'].replace({0: "Fake", 1: "Real"}, inplace=True)
    
    value_count = final_result['Fake/Real'].value_counts()
    #print(value_count)
    #print(value_count.to_dict())
    dict_result = value_count.to_dict()
    #print(type(dict_result))
    return redirect(url_for('graph',data = dict_result, values = value_count["Fake"]))
    #return render_template("index.html", result = final_result.to_html(classes='table table-dark table-striped'))

@app.route('/about')  
def about():  
    return render_template("about.html"); 

@app.route('/graph')
def graph():
    data = request.args.get('data', None)
    value = request.args.get('values', None)
    res = eval(data)
    #res['Task'] = 'Fake/Real Reviews Present'
    #print(type(res))
    #print(value)
    return render_template('graph.html', data = res, values = value) 

if __name__ == '__main__':
    app.run(debug=True)  