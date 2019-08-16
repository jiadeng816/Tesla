# 查询操作

import pymysql
import jieba
import re

jieba.load_userdict("data/dict/carType.txt")
with open("data/dict/carType.txt", "r", encoding="utf-8") as f:
    carList = [i.replace("\n", "") for i in f.readlines()]

parameterDict = {
    "GuidancePrice": ["价格", "多少钱", "怎么卖"],
    "EngineType": ["发动机", "排量", "马力"],
    "Gearbox": ["离合器", "变速箱"],
    "Structure": ["车型", "外形", "几座", "两厢车", "三厢车", "SUV"]
}

parameter2resultDict = {
    "GuidancePrice": "价格",
    "EngineType": "发动机类型",
    "Gearbox": "离合器类型",
    "Structure": "车型"
}

def list2str(reList):
    result = ""
    for i in reList:
        result = result + i + "|"
    return result[:-1]

def reString():
    parameterReDict = {}
    carReString = list2str(carList)
    for k, v in parameterDict.items():
        parameterReDict[k] = list2str(v)
    return carReString, parameterReDict

carReString, parameterReDict = reString()

# 打开数据库连接
db = pymysql.connect(host="localhost", user="root",
                     password="12345", db="cars", port=3306)

# 使用cursor()方法获取操作游标
cur = db.cursor()

class KBSearch():
    @classmethod
    def DBSearch(cls, car_type, parameter4search, parameterList):
        sql = "SELECT CarType,{} FROM cars.car_parameter WHERE CarType LIKE '%{}%'".format(parameter4search, car_type)
        try:
            cur.execute(sql)  # 执行sql语句
            results = list(cur.fetchall())  # 获取查询的所有记录
            resultString = results[0][0] + "的"
            for i in range(len(parameterList)):
                resultString = resultString + parameter2resultDict[parameterList[i]] + "是：" + results[0][i+1] + "，"
            return resultString[:-1]
        except:
            return None

class KBAnalysis():
    @classmethod
    def analysis(cls, data):
        car_type = re.search(carReString, data).group() if re.search(carReString, data) else None
        parameterList = []
        parameter4search = ""
        for k, v in parameterReDict.items():
            if re.search(v, data):
                parameterList.append(k)
                parameter4search = parameter4search + k + ","
        parameter4search = parameter4search[:-1]
        # print("car_type", car_type)
        # print("parameter4search", parameter4search)
        # print("parameterList", parameterList)
        answer = KBSearch.DBSearch(car_type, parameter4search, parameterList)
        return answer