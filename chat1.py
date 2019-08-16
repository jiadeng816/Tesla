# coding:utf-8
from flask import Flask,render_template,request as req,redirect,url_for
import json
import urllib
import urllib.request
from collections import defaultdict
import time, random
from KBAnswer import KBAnalysis



app = Flask(__name__)

@app.route("/")
def show():
    return render_template("communication1.html")


@app.route('/chat', methods=['GET', 'POST'])
def index():
    if req.method == 'POST':
        UNKList = ["这个问题我不知道哎┑(￣Д ￣)┍", "这个我不太懂~", "你的问题太难了/(ㄒoㄒ)/~~", "容我再学习一下", "这可把我问住了…"]
        data = req.form.get("chat")

        # # 这里是相似度计算返回的答案
        # answerList = SimAnswer.findAnswer(data)
        # print("query: ", data)
        # print("answer: ", answerList)
        # if answerList[0]["value"] > 0.92:       # 这里的阈值需要测试一下
        #     answer = answerList[0]["answer"]
        # else:
        #     answer = random.choice(UNKList)

        # 这里是数据库查询返回的答案
        answer = KBAnalysis.analysis(data) if KBAnalysis.analysis(data) else "这个问题我不知道"

        # 拼接答案并输出返回值
        context={
            'response': answer
        }
        time.sleep(random.randint(1,10)/10)
        return json.dumps(context)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
