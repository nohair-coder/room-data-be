# coding: utf8
import socketserver
import threading
import time
import ast

from .Httpsend import dataPost
from ..WLAN_4G import Analysis_4G

exit_flag = False
timer_cnt = 0
udp_server = 0
Addr_4G = 0


class MySocket(socketserver.BaseRequestHandler):

    def handle(self):
        global udp_server
        global Addr_4G
        try:
            data = self.request[0].decode()
            print(data)
            Addr_4G = self.client_address
            udp_server = self.request[1]
            if data[0] == '{' and data[-1] == '}':
                Analysis_4G.Recv_4G_Queue.put(data)
            else:
                print('error Recv')
        except:
            print(self.request[0].decode(), '-------------------MySocket Error')


def Init_4GSocket():
    """4G Socket 初始化"""
    Send_4G_Thread = threading.Thread(target=Send_4G)
    Send_4G_Thread.start()
    server = socketserver.ThreadingUDPServer(('0.0.0.0', 8200), MySocket)
    server.serve_forever()


def Send_4G():
    """4G发送"""
    global Addr_4G
    print(threading.current_thread().name, 'Send_4G is running...')
    while not exit_flag:
        data = Analysis_4G.Send_4G_Queue.get(block=True)
        udp_server.sendto(data.encode(), Addr_4G)
        time.sleep(0.1)


def Handle_4G():
    """处理命令"""
    print(threading.current_thread().name + 'running...')
    while not exit_flag:
        try:
            msg = Analysis_4G.Recv_4G_Queue.get()
            if msg is not None:
                if msg[0] == '{' and msg[-1] == '}':
                    data = ast.literal_eval(msg)
                    Analysis_4G.network_management(data['node'])
                    Analysis_4G.dataAnalyse(data)
                else:
                    print('Handle_4G error --- can not identify !')
        except:
            print('Handle_4G error')


def serverSend():
    """上传数据"""
    print('serverSend is running...')
    while not exit_flag:
        try:
            data_obj = Analysis_4G.serverSendQueue.get(timeout=3)
            print(data_obj)
            dataPost(data_obj)
            # if not dataPost(data_obj):
            #     print('serverSend Error')
            # Analysis_4G.serverSendQueue.put(data_obj)
        except:
            pass


def timer():
    """定时任务"""
    global timer_cnt
    while not exit_flag:
        timer_cnt += 1
        if timer_cnt > 10000:
            timer_cnt = 0
        if timer_cnt % 100 == 1:
            Analysis_4G.nodeMonitor()
        if timer_cnt % 600 == 1:
            Analysis_4G.timeoutHandler()
        time.sleep(1)


socket_4G_thread = threading.Thread(target=Init_4GSocket)
socket_4G_thread.start()
Hand4GThread = threading.Thread(target=Handle_4G)
Hand4GThread.start()
serverSendThread = threading.Thread(target=serverSend)
serverSendThread.start()
timer_thread = threading.Thread(target=timer)
timer_thread.start()
