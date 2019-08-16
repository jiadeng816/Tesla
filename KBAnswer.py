# 查询操作

import pymysql
import jieba
import re

jieba.load_userdict("data/dict/carType.txt")
with open("data/dict/carType.txt", "r", encoding="utf-8") as f:
    carList = [i.replace("\n", "") for i in f.readlines()]

parameterDict = {
    "GuidancePrice": ["价格", "多少钱", "怎么卖", "贵不贵"],
    "Manufacturer": ["制造商", "厂家", "什么(.*)生产", "哪里(.*)生产"],
    "EnergyType": ["能源", "动力", "汽油", "燃油", "新能源"],
    "ProductDate": ["(时候|时间)(.*)(上市|发行|推出|销售)", "(上市|发行|推出|销售)(.*)(时候|时间)"],
    "Power": ["功率", "马力"],
    "MaxTorque": ["扭矩"],
    "EngineType": ["发动机", "排量"],
    "Gearbox": ["离合器", "变速箱"],
    "Structure": ["车型", "外形", "几座", "两厢车", "三厢车", "SUV"],
    "MaxSpeed": ["时速", "车速", "速度"],
    "OilConsumptionTheory": ["油耗", "耗油"],
    "MaintenanceCycle": ["(保|首保|保养)(.*)(周期|年限|距离|公里)"]
}

parameter2resultDict = {
    "GuidancePrice": "价格",
    "Manufacturer": "制造商",
    "EnergyType": "能源类型",
    "ProductDate": "上市时间",
    "Power": "最大功率",
    "MaxTorque": "最大扭矩",
    "EngineType": "发动机类型",
    "Gearbox": "离合器类型",
    "Structure": "车型",
    "MaxSpeed": "最大时速",
    "OilConsumptionTheory": "理论油耗",
    "MaintenanceCycle": "首保周期"
}

measureUnitDict = {
    "GuidancePrice": "万元",
    "Power": "kW",
    "MaxTorque": "N·m",
    "Size": "mm",
    "MaxSpeed": "km/h",
    "OilConsumptionTheory": "L/100km"
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
    def answer2string(cls, key, answer):
        if key == "ProductDate":
            return str(int(answer))[:4]+"年"+str(int(answer))[4:6]+"月"
        elif key in measureUnitDict:
            return answer + measureUnitDict[key]
        else:
            return answer

    @classmethod
    def DBSearch(cls, car_type, parameter4search, parameterList):
        if car_type and parameter4search:
            sql = "SELECT CarType,{} FROM cars.car_parameter WHERE CarType LIKE '%{}%'".format(parameter4search, car_type)
            cur.execute(sql)  # 执行sql语句
            results = list(cur.fetchall())  # 获取查询的所有记录
            if not results or None in results[0]:
                return "没有查到相关数据!"
            else:
                resultString = results[0][0] + "的"
                for i in range(len(parameterList)):
                    resultString = resultString + parameter2resultDict[parameterList[i]] + "是：" + \
                                   cls.answer2string(parameterList[i], results[0][i+1]) + "，"
                return resultString[:-1]
        else:
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