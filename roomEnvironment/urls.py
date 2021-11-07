"""roomEnvironment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, re_path, path

from rest_framework.routers import DefaultRouter

from apps.WLAN_4G import views  # 4G通信入口，导入即可

from apps.envdata.views import DataView, get_now_data, get_range_data, get_now_voltage
from apps.room.views import RoomView
from apps.room.views import get_nodes

router = DefaultRouter()
# 配置环境数据的url
router.register(r'data', DataView)
router.register(r'node', RoomView)

urlpatterns = [
    re_path('^', include(router.urls)),
    path('getNowData/', get_now_data),
    path('getRangeData/', get_range_data),
    path('getNodes/', get_nodes),
    path('getVoltage/', get_now_voltage)
]
