# Python3 샘플 코드 #
import requests
import json
import xmltodict
from db_connect import db
from models import Question
from datetime import datetime
from flask import g
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

def remove_tag(content):
    if content is not None:
        content = re.sub('<p>', '', content)
        content = re.sub('</p>', '', content)
        # print(type(content))
        # print(content)
    return content

def initial_insert(url, params):
    user = User(username='admin',
                        password=generate_password_hash('1234'),
                        email='admin@gmail.com')
    db.session.add(user)
    db.session.commit()

    for i in range(1, 5):
        params['pageNo'] = i;
        response = requests.get(url, params=params)
        result = response.content.decode()
        jsonString = json.dumps(xmltodict.parse(result), indent=4)
        dict = json.loads(jsonString)['response']['body']['items']['item']

        for j in range(9):
            tmp = dict[j]
            print(type(tmp))
            print(tmp)

            question = Question(entpName=remove_tag(tmp['entpName']),
                                    itemName=remove_tag(tmp['itemName']), efcyQesitm=remove_tag(tmp['efcyQesitm']),
                                    useMethodQesitm=remove_tag(tmp['useMethodQesitm']), atpnQesitm=remove_tag(tmp['atpnQesitm']),
                                    depositMethodQesitm=remove_tag(tmp['depositMethodQesitm']), create_date=datetime.now(), user=user)
            db.session.add(question)
            db.session.commit()



url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
params ={'serviceKey' : 'kQ4M06xZZQmh7mwbNBpWs2PLjyMWRMVYdQ6EJB26Wxx0zucRb7Oc8zyDrqY1ACCOlGd7c1Oirdx/2cJK/MxsTA==', 'pageNo' : '1', 'numOfRows' : '9', '_returnType' : 'xml' }

# initial_insert(url, params)

# print(type(dict))
# print(dict)
