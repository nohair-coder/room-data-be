from rest_framework import viewsets
from .models import Envdata
from ..room.models import Room
from .serializers import EnvDataSerializer
from django.http import JsonResponse
from django.db.gmodels import Q
import json
import datetime
import re


# Create your views here.


class DataView(viewsets.ModelViewSet):
    queryset = Envdata.objects.all()
    serializer_class = EnvDataSerializer
    # filter_fields = ['stationId', 'pigId', "earId"]
    # ordering_fields = 'stationId'


# 获取当前每个节点的环境参数
def get_now_data(request):
    if request.method == 'GET':
        all_room = Room.objects.all().values('allRooms')
        now_data = []
        for item in all_room:
            one = Envdata.objects.filter(node=item['allRooms']).order_by('-dateTime').first()
            now_data.append(
                {'node': item['allRooms'],
                 'carbon': one.carbon,
                 'humidity': one.humidity/10,
                 'light': one.light/10,
                 'temperature': one.temperature/10,
                 'wind': one.wind/10,
                 'status': one.status}
            )
        print(now_data)
        return JsonResponse({'nowData': now_data}, status=200)


# 根据时间范围获取节点环境参数，用于前端图表绘制
def get_range_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        node = data.get('node')
        startDate = re.findall(r"^(\d+)-(\d+)-(\d+)$", data.get('startDate'))[0]
        startTime = re.findall(r"^(\d+):(\d+)$", data.get('startTime'))[0]
        endDate = re.findall(r"^(\d+)-(\d+)-(\d+)$", data.get('endDate'))[0]
        endTime = re.findall(r"^(\d+):(\d+)$", data.get('endTime'))[0]
        start = datetime.datetime(year=int(startDate[0]), month=int(startDate[1]), day=int(startDate[2]),
                                  hour=int(startTime[0]), minute=int(startTime[1]))
        end = datetime.datetime(year=int(endDate[0]), month=int(endDate[1]), day=int(endDate[2]), hour=int(endTime[0]),
                                minute=int(endTime[1]))
        cur = True if (end - start).days >= 3 else False
        rangeData = Envdata.objects.filter(Q(node=node), Q(dateTime__range=(start, end))).order_by('dateTime')
        dateTimeArray = []
        carbonArray = []
        humidityArray = []
        lightArray = []
        temperatureArray = []
        windArray = []
        for item in rangeData:
            dateTimeArray.append(item.dateTime)
            carbonArray.append(item.carbon)
            humidityArray.append(item.humidity/10)
            lightArray.append(item.light/10)
            temperatureArray.append(item.temperature/10)
            windArray.append(item.wind)
        return JsonResponse(
            {
                'cur': cur,
                'dateTimeArray': dateTimeArray,
                'carbonArray': carbonArray,
                'humidityArray': humidityArray,
                'lightArray': lightArray,
                'temperatureArray': temperatureArray,
                'windArray': windArray,
            }, status=200)
            
            
def get_now_voltage(request):
    if request.method == 'GET':
        all_room = Room.objects.all().values('allRooms')
        NowVoltage = []
        for item in all_room:
            one = Envdata.objects.filter(node=item['allRooms']).order_by('-dateTime').first()
            NowVoltage.append(
                {
                    'node': item['allRooms'],
                    'voltage': one.voltage/10,
                    'status': one.status
                }
            )
        print(NowVoltage)
        return JsonResponse({'nowVoltage': NowVoltage}, status=200)
