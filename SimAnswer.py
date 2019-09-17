# coding:utf-8

import json
from json2vec import Query2Vec
import numpy as np


class SimAnswer:
    @classmethod
    def load_data(cls):
        with open("data/QA_data/QA_vec.txt", "r", encoding="utf-8") as f:
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
    answer = SimAnswer.findAnswer("什么是珠光漆")
    print(answer)