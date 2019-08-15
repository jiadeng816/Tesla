# coding:utf-8
from flask import Flask,render_template,request as req,redirect,url_for
import json
import urllib
import urllib.request
from collections import defaultdict
import time, random
from SimAnswer import SimAnswer
from KBAnswer import KBAnswer
import jieba

jieba.load_userdict("data/dict/carType.txt")
with open("data/dict/catType.txt", "r", encoding="utf-8") as f:
    carList = [i.replace("\n", "") for i in f.readlines()]
priceList = ["价格", "多少钱", "怎么卖"]

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
        flag = 0
        answer = None
        car_type = None
        for query in jieba.cut(data):
            if query in priceList:
                flag += 1
            if query in carList:
                car_type = query
                flag += 1
            if flag == 2:
                answer = KBAnswer.DBSearch(car_type)
                break
        answer = answer if answer else "这个问题我不知道"

        # 拼接答案并输出返回值
        context={
            'response': answer
        }
        time.sleep(random.randint(1,15)/10)
        return json.dumps(context)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
