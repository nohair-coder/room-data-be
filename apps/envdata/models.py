from django.db import models
from ..room.models import Room


# Create your models here.
class Envdata(models.Model):
    node = models.ForeignKey(Room, to_field='allRooms', on_delete=models.CASCADE)
    carbon = models.IntegerField()  # 二氧化碳
    humidity = models.IntegerField()  # 湿度
    light = models.IntegerField()  # 光照
    temperature = models.IntegerField()  # 温度
    wind = models.IntegerField()  # 风速
    dateTime = models.DateTimeField()  # 时间,结合node防止重复存数据
    voltage = models.IntegerField()  # 电压
    status = models.SmallIntegerField(default=0)  # 工作状态，1代表开机，0代表关机

    class Meta:
        db_table = 'EnvData'  # 指明数据库表名
        verbose_name = '环境参数表'  # 在admin站点中显示的名称

        # unique_together = ('node', 'dateTime')

        # verbose_name_plural = verbose_name  # 显示的复数名称


# data = {
#     'node': 1,
#     'carbon': 20,
#     'humidity': 20,
#     'light': 20,
#     'temperature': 20,
#     'wind': 20,
#     'dateTime': '202011191050'
# }
