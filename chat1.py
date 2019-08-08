# coding:utf-8
from flask import Flask,render_template,request as req,redirect,url_for
import json
import urllib
import urllib.request
from collections import defaultdict
import time, random
from SimAnswer import SimAnswer

app = Flask(__name__)

@app.route("/")
def show():
    return render_template("communication1.html")


def load_data():
    qa = defaultdict(lambda: "这个问题我不太清楚哎")
    with open("data/baike_data.txt", "r", encoding="utf-8") as f:
        baike_data = json.load(f)
        for i in range(len(baike_data)):
            for data in baike_data[i]["data"]:
                 qa[data["query"]] = data["answer"]
    with open("data/greeting.txt", "r", encoding="utf-8") as f:
        baike_data = json.load(f)
        for i in range(len(baike_data)):
            for data in baike_data[i]["data"]:
                 qa[data["query"]] = data["answer"]
    return qa


@app.route('/chat', methods=['GET', 'POST'])
def index():
    if req.method == 'POST':
        global data
        data = req.form.get("chat")
        answer = qa[data]
        # answer = SimAnswer.findAnswer(data)
        context={
            'response': answer
        }
        time.sleep(random.randint(1,15)/10)
        return json.dumps(context)

if __name__ == '__main__':
    qa = load_data()
    app.run(debug=True, host="0.0.0.0", port=5000)
