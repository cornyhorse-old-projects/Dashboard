from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save

User = get_user_model()


# Create your models here.
# class UserProfile(models.Model):
#    user = models.OneToOneField(User,on_delete=models.CASCADE)
#    pair = models.ManyToManyField('self' ,through='PairData', symmetrical=False)

# def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        profile, created = UserProfile.objects.get_or_create(user=instance)
# post_save.connect(create_user_profile, sender=User)

class Network(models.Model):
    network_name = models.CharField(max_length=255)
    network_description = models.TextField(null=True, blank=True)
    located_in_cloud = models.BooleanField()
    #owners = models.ManyToManyField(User)
    owners = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.network_name


# class NetworkOwner(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     network = models.ForeignKey(Network, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}: {}'.format(self.owner_id, self.network.network_name)


class ComputeResource(models.Model):
    network = models.ForeignKey(
        Network, on_delete=models.CASCADE
    )  # , null=True, blank=True)
    resource_name = models.CharField(max_length=255, null=True, blank=True)
    portable = models.BooleanField(blank=True, null=True)
    local_ipv4_address = models.GenericIPAddressField(
        protocol="IPv4", blank=True, null=True
    )
    local_ipv6_address = models.GenericIPAddressField(
        protocol="IPv6", blank=True, null=True
    )
    external_ipv4_address = models.GenericIPAddressField(
        protocol="IPv4", blank=True, null=True
    )
    external_ipv6_address = models.GenericIPAddressField(
        protocol="IPv6", blank=True, null=True
    )
    powered_on = models.BooleanField(blank=True, null=True)
    powered_on_utc = models.DateTimeField(default=datetime.now, blank=True, null=True)
    uptime = models.DurationField(blank=True, null=True)
    last_seen = models.DateTimeField(default=datetime.now, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.network:
            return "{} ({})".format(self.resource_name, self.network.network_name)
        else:
            return self.resource_name

class Sensor(models.Model):
    # This is the sensor/adapter itself.
    sensor_name = models.CharField(max_length=255)
    adapter_type = models.CharField(max_length=255)

    def __str__(self):
        return "{} ({})".format(self.sensor_name, self.adapter_type)


class ComputeSensor(models.Model):
    # The relationship between a compute resource and the sensor
    compute = models.ForeignKey(ComputeResource, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.compute.resource_name, self.sensor.sensor_name)


class SensorHeartbeat(models.Model):
    # This the the actual, raw measurement
    compute_sensor = models.ForeignKey(ComputeSensor, on_delete=models.CASCADE)
    heartbeat_utc = models.DateTimeField()
    raw = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.compute_sensor.compute_id, self.heartbeat_utc)


class Measurement(models.Model):
    # This is the type of measurement
    computesensor = models.ForeignKey(ComputeSensor, on_delete=models.CASCADE)
    measurement_name = models.CharField(max_length=25, blank=True, null=True)
    unit = models.CharField(max_length=15)

    def __str__(self):
        return self.measurement_name


class SensorMeasurement(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    heartbeat = models.ForeignKey(SensorHeartbeat, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return "{} ({} - {}): {}".format(
            self.heartbeat.compute_sensor.compute.resource_name,
            self.measurement.measurement_name,
            self.heartbeat.heartbeat_utc,
            self.value,
        )
