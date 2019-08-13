# conding : utf-8


from bs4 import BeautifulSoup
import requests
import json
import re

def textRmSpace(text):
    '''替换文本中的转义字符和空格'''
    return text.replace('\n', '').replace('\t', '').replace('\r', '').replace('\v', '').replace('\u3000', '').replace(
        ' ', '').replace("\xa0", "").replace("[汽车之家百科]", "")


def textRmBrackets(text):
    '''利用正则表达式去掉文本中括号和特殊字符之间的文字'''
    result_en = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", text)
    result = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】|\\·.*?·", "", result_en)
    if '分类标签' in result:
        result = result[:result.find('分类标签')]
    return result


def urlParse(url):
    '''相应url请求并解析成html代码'''
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def spaceJoin(text):
    answerList = text[text.find("]") + 1:].split()
    answerFirst = answerList[0]
    for i in range(1, len(answerList)):
        if ('\u0041' <= answerList[i][1] <= '\u005a') or ('\u0061' <= answerList[i][1] <= '\u007a'):
            answerFirst = answerFirst + " " + answerList[i]
    return answerFirst


def findQA(url):
    soup = urlParse(url)
    data = soup.find_all('div', {'class': 'info'})
    result = []
    for i in data:
        try:
            query = i.find_all('p', {'class': 'tit'})[0].text
            answer = i.find_all('p', {'class': 'intro'})[0].text
            answerFirst = spaceJoin(answer)
            answerFirst = answerFirst[0: answerFirst.rfind("。")+1]
            result.append({"query": textRmSpace(query), "answer": answerFirst})
        except:
            continue
    return result


def nextPage(baseURL, url):
    soup = urlParse(url)
    try:
        nextPage = soup.find('div', {'class': 'athm-page__info'}).text.split()
        if nextPage:
            next_url = soup.find('a', {'class': 'athm-page__next'}).attrs["href"]
            if "baike" in next_url:
                return baseURL +  next_url
            else:
                return None
        else:
            return None
    except:
        return None


def staticsURL(baseURL):
    resultDict = []
    urlDict = {"选车":3, "买车":5, "用车":6, "参数详解":7, "配置详解":8, "汽车术语":9, "汽车文化":10}
    for k, v in urlDict.items():
        print(k, v)
        result_all = []
        url = baseURL + "/baike/detail_{}_0_0.html#pvareaid=2042417".format(v)
        result = findQA(url)
        result_all.extend(result)
        url = nextPage(baseURL, url)
        while url:
            result = findQA(url)
            result_all.extend(result)
            url = nextPage(baseURL, url)
        resultDict.append({"category":k, "data":result_all})
    with open("../data/QA_data/baike_data.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(resultDict, ensure_ascii=False))


if __name__ == '__main__':
    BASE_URL = "https://car.autohome.com.cn"
    staticsURL(BASE_URL)


