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


@app.route('/chat', methods=['GET', 'POST'])
def index():
    if req.method == 'POST':
        global data
        data = req.form.get("chat")
        answerList = SimAnswer.findAnswer(data)
        print("query: ", data)
        print("answer: ", answerList)
        answer = answerList[0]["answer"]
        context={
            'response': answer
        }
        time.sleep(random.randint(1,15)/10)
        return json.dumps(context)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
