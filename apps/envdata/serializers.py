from rest_framework import serializers
from .models import Envdata


class EnvDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envdata
        fields = '__all__'
