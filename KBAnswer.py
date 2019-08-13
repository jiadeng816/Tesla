# 查询操作

import pymysql  # 导入 pymysql

# 打开数据库连接
db = pymysql.connect(host="localhost", user="root",
                     password="12345", db="cars", port=3306)

# 使用cursor()方法获取操作游标
cur = db.cursor()

class KBAnswer():
    @classmethod
    def DBSearch(cls, data):
        sql = "SELECT CarType,GuidancePrice FROM cars.car_parameter WHERE CarType LIKE '%{}%'".format(data)
        try:
            cur.execute(sql)  # 执行sql语句
            results = list(cur.fetchall())  # 获取查询的所有记录
            if results:
                return results[0][0] + "的价格是" + results[0][1] + "万元"
            else:
                return None
        except Exception as e:
            raise e
