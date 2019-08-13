# -*- coding: utf-8 -*-

# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")


# 初始化数据库连接，使用pymysql模块
db_info = {'user': 'root',
           'password': '12345',
           'host': 'localhost',
           'port': 3306,
           'database': 'cars'
           }

engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info, encoding='utf-8')

# 读取本地CSV文件
df = pd.read_csv("../data/dataframe/car_parameter.csv", sep=',', encoding="utf-8")

# # 这里是从df中导出汽车的类型名称
# carType = df["CarType"]
# result = set({})
# for tp in carType:
#     name = tp.split()[0]
#     result.add(name)
# result = [i+"\n" for i in list(result)]
# print(result)
# with open("../data/dataframe/catType.txt", "w", encoding="utf-8") as f:
#     f.writelines(result)

df.to_sql('car_parameter', con=engine,  if_exists='replace')
print("Write to MySQL successfully!")
