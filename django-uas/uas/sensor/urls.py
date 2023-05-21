from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),

    path('farm/humidity', views.Sensor1View.as_view()),
    path('farm/acidity', views.Sensor2View.as_view()),
    path('farm/quality', views.Sensor3View.as_view()),
    path('actuator/actuator1', views.ActuatorView.as_view()),
]