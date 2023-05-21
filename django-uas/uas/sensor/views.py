from django.shortcuts import render
from django.views.generic import View
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import paho.mqtt.client as mqtt

from ml_model import machinelearning

from .serializers import SensorSerializer, ActuatorSerializer
from .models import Sensor, Actuator


# Create your views here.
def index(request):
    farm_hum = Sensor.objects.get(name="farm_hum")
    farm_aci = Sensor.objects.get(name="farm_aci")
    farm_qua = Sensor.objects.get(name="farm_qua")

    actuator1 = Actuator.objects.get(name="actuator1")

    ml_value = machinelearning.ml_waterflow
    predict = ml_value.predict([float(farm_hum.value), float(farm_aci.value), float(farm_qua.value)])

    farm_aci = round(float(farm_aci.value), 2)

    actuator1.state = int(predict)
    actuator1.save()

    serializer = ActuatorSerializer(actuator1, data=predict, partial=True)
    if serializer.is_valid():
        serializer.save()
    
    context = {
        'farm_hum': str(farm_hum.value),
        'farm_aci': str(farm_aci),
        'farm_qua': str(farm_qua.value),

        "predict" : str(predict[0][0]),
        "state"   : actuator1.state
    }

    return render(request, 'index.html', context)


class Sensor1View(APIView):
    sensor_name = "farm_hum"
    def get(self, request, format=None):
        sensor1 = Sensor.objects.get(name=self.sensor_name)
        data = {
            "value": sensor1.value
        }
        return Response(data)

class Sensor2View(APIView):
    sensor_name = "farm_aci"
    def get(self, request, format=None):
        sensor2 = Sensor.objects.get(name=self.sensor_name)
        sensor2 = round(float(sensor2.value), 2)
        data = {
            "value": sensor2
        }
        return Response(data)

class Sensor3View(APIView):
    sensor_name = "farm_qua"
    def get(self, request, format=None):
        sensor3 = Sensor.objects.get(name=self.sensor_name)
        data = {
            "value": sensor3.value
        }
        return Response(data)

class ActuatorView(APIView):
    actuator_name = "actuator1"
   
    def get(self, request, format=None):
        actuator1 = Actuator.objects.get(name=self.actuator_name)
        farm_hum = Sensor.objects.get(name="farm_hum")
        farm_aci = Sensor.objects.get(name="farm_aci")
        farm_qua = Sensor.objects.get(name="farm_qua")

        ml_value = machinelearning.ml_waterflow
        predict = ml_value.predict([float(farm_hum.value), float(farm_aci.value), float(farm_qua.value)])
        actuator1.state = int(predict)
        actuator1.save()

        data = {
            "value": actuator1.state
        }
        return Response(data)

def on_message_hum(client, userdata, msg):
    farm_hum = Sensor.objects.get(name="farm_hum")
    data = {
        'value': msg.payload.decode('utf-8')
    }
    serializer = SensorSerializer(farm_hum, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    print('received a new SOIL HUMIDITY data ', msg.payload.decode('utf-8'))
    
def on_message_aci(client, userdata, msg):
    farm_aci = Sensor.objects.get(name="farm_aci")
    data = {
        'value': msg.payload.decode('utf-8')
    }
    serializer = SensorSerializer(farm_aci, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    print('received a new SOIL ACIDITY data ', msg.payload.decode('utf-8'))
     
def on_message_qua(client, userdata, msg):
    farm_qua = Sensor.objects.get(name="farm_qua")
    data = {
        'value': msg.payload.decode('utf-8')
    }
    serializer = SensorSerializer(farm_qua, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    print('received a new WATER QUALITY data ', msg.payload.decode('utf-8'))


client = mqtt.Client("sensor")

client.message_callback_add('farm/humidity', on_message_hum)
client.message_callback_add('farm/acidity', on_message_aci)
client.message_callback_add('farm/quality', on_message_qua)

client.connect('localhost', 1883)
client.loop_start()
client.subscribe('#')