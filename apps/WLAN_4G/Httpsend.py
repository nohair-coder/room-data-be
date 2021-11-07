# coding: utf8
import requests
import json

baseURL = 'http://localhost:8056/'


def dataPost(json_object):
    """数据上传"""
    try:
        r = requests.post(baseURL + 'data/', json=json_object)
        # r = requests.post("http://httpbin.org/post", data=payload)
        ack = json.loads(r.text)
        print('dataPost success')
    except:
        print('dataPost failed !')
        return False


def devicePost(json_object):
    """节点新增"""
    try:
        r = requests.post(baseURL + 'node/', json=json_object)
        ack = json.loads(r.text)
        print('devicePost success')
    except:
        print('devicePost connect failed !')
        return False

