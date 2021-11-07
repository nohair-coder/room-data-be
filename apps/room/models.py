from django.db import models


# Create your models here.
class Room(models.Model):
    allRooms = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'Room'  # 指明数据库表名
        verbose_name = '节点列表'  # 在admin站点中显示的名称
