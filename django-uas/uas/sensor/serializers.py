from rest_framework import serializers

from .models import Sensor, Actuator

        
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        
        fields = "__all__"

class ActuatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actuator
        
        fields = "__all__"