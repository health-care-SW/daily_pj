# Python3 샘플 코드 #
import requests
import json
import xmltodict


url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
params ={'serviceKey' : 'kQ4M06xZZQmh7mwbNBpWs2PLjyMWRMVYdQ6EJB26Wxx0zucRb7Oc8zyDrqY1ACCOlGd7c1Oirdx/2cJK/MxsTA==', 'pageNo' : '1', 'numOfRows' : '5', '_returnType' : 'xml' }
response = requests.get(url, params=params)
result = response.content.decode()
jsonString = json.dumps(xmltodict.parse(result), indent=4)
dict = json.loads(jsonString)


print(type(dict))
print(dict['response']['body']['items']['item'][0])
print(dict['response']['body']['items']['item'][1])
