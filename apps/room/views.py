from rest_framework import viewsets
from .models import Room
from .serializers import RoomSerializer
from django.http import JsonResponse
# Create your views here.


# 序列化
class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # filter_fields = ['stationId', 'pigId', "earId"]
    # ordering_fields = 'stationId'


# 获取所有节点
def get_nodes(request):
    if request.method == 'GET':
        all_room = Room.objects.all().values('allRooms')
        all_nodes = []
        for item in all_room:
            all_nodes.append(item['allRooms'])
        return JsonResponse({'allNodes': all_nodes}, status=200)
