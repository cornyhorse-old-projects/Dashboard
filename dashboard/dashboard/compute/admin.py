from django.contrib import admin
from .models import Network, ComputeResource, Sensor, ComputeSensor, SensorHeartbeat, SensorMeasurement, Measurement
# Register your models here.


admin.site.register(Network)
admin.site.register(ComputeResource)
admin.site.register(ComputeSensor)
admin.site.register(Sensor)
admin.site.register(SensorHeartbeat)
admin.site.register(SensorMeasurement)
admin.site.register(Measurement)
