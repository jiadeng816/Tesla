# coding:utf-8

from collections import defaultdict
import json
from json2vec import Query2Vec
import numpy as np

# def load_data():
#     qa = defaultdict(lambda: "这个问题我不太清楚哎")
#     with open("data/baike_data.txt", "r", encoding="utf-8") as f:
#         baike_data = json.load(f)
#         for i in range(len(baike_data)):
#             for data in baike_data[i]["data"]:
#                  qa[data["query"]] = data["answer"]
#     with open("data/greeting.txt", "r", encoding="utf-8") as f:
#         baike_data = json.load(f)
#         for i in range(len(baike_data)):
#             for data in baike_data[i]["data"]:
#                  qa[data["query"]] = data["answer"]
#     return qa


class SimAnswer:
    @classmethod
    def load_data(cls):
        with open("data/QA_vec.txt", "r", encoding="utf-8") as f:
            QA_data = json.load(f)
            QA_list = []
            for i in range(len(QA_data)):
                QA_list.extend(QA_data[i]["data"])
        return QA_list

    @classmethod
    def cos_sim(cls, vector_a, vector_b):
        vector_a = np.mat(vector_a)
        vector_b = np.mat(vector_b)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = num / denom
        sim = 0.5 + 0.5 * cos
        return sim

    @classmethod
    def similaritySort(cls, query_vec):
        queryVecDict = cls.load_data()
        for i in range(len(queryVecDict)):
            value = cls.cos_sim(query_vec, queryVecDict[i]["vec"])
            queryVecDict[i]["value"] = value
            del queryVecDict[i]["vec"]
        queryVecDict.sort(key=lambda x: x["value"], reverse=True)
        return queryVecDict[:3]

    @classmethod
    def findAnswer(cls, data):
        q2v = Query2Vec(data)
        data_vec = q2v.query2vec()
        return cls.similaritySort(data_vec)


if __name__ == "__main__":
    SimAnswer.findAnswer("你好")