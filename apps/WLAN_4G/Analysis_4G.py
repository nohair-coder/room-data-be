# coding: utf8
import time
import datetime
import queue

from ..room.models import Room
from .Httpsend import devicePost


device_status = {}  # 设备缓存
Send_4G_Queue = queue.Queue(32)
Recv_4G_Queue = queue.Queue(64)
dataRequestQueue = queue.Queue(32)

serverSendQueue = queue.Queue()


def responseMsg(node):
    id_ack = node+' OK'
    return id_ack


def dataAnalyse(data):
    """数据包解析"""
    data_object = {}
    node_id = data['node']  # 获得节点ID
    if True:
        try:
            data_object['node'] = node_id
            data_object['carbon'] = data['c']
            data_object['humidity'] = data['h']
            data_object['light'] = data['l']
            data_object['temperature'] = data['t']
            data_object['wind'] = data['w']
            data_object['voltage'] = data['u']  # 电压
            data_object['status'] = 1  # 正常工作中
            data_object['dateTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(data['d'], "%Y%m%d%H%M%S"))
        except:
            print('data  Analyse  Error')
            data_object = {}
    if data_object != {}:
        serverSendQueue.put(data_object)
        Send_4G_Queue.put(responseMsg(node_id))
    else:
        print('dataAnalyse  data_obj is null')


def timeoutHandler():
    """接收超时处理"""
    global device_status
    for key in device_status:
        if device_status[key]['work_status'] == 'ON':  # 正在接收中
            device_status[key]['socket_status'] -= 1
            if device_status[key]['socket_status'] <= 0:
                device_status[key]['work_status'] = 'OFF'
        if device_status[key]['work_status'] == 'OFF':  # 正在接收中
            data_object = {
                'node': key,
                'carbon': 0,
                'humidity': 0,
                'light': 0,
                'temperature': 0,
                'wind': 0,
                'voltage': 0,
                'status': 0,
                'dateTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            serverSendQueue.put(data_object)


def nodeMonitor():
    """节点监控定时函数"""
    # 此函数由定时任务调用
    global device_status
    print("device_status:", device_status)


def network_management(node):
    """节点状态"""
    global device_status
    if node not in device_status:  # 新建一个设备缓存
        device_status[node] = {
            "work_status": 'ON',  # 饲喂站工作状态
            "socket_status": 2,  # 网络通信状态
        }
        json_object = {
            'allRooms': node,
        }
        devicePost(json_object)  # 上传新建的设备状态
    device_status[node]['work_status'] = 'ON'
    device_status[node]['socket_status'] = 2


def Analysis_sysInit(func):
    """设备状态初始化"""
    global device_status
    for i in func():
        device_status[i] = {
            "socket_status": 0,  # 网络通信状态
            "work_status": 'OFF',  # 节点工作状态
        }


def get_nodes_list():
    # 获取阅读量最多的5条数据
    stations = Room.objects.values('allRooms')  # 取节点号
    s_list = []
    for item in stations:
        s_list.append(item['allRooms'])
    return s_list


Analysis_sysInit(get_nodes_list)
