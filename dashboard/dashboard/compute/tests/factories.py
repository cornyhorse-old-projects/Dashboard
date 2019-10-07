from factory import DjangoModelFactory, SubFactory, Faker, post_generation
from ..models import Network, ComputeResource
from django.contrib.auth import get_user_model
from typing import Any, Sequence
from faker import Faker as FakerForDate

fake = FakerForDate()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(extra_kwargs={})
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class NetworkFactory(DjangoModelFactory):
    network_name = 'Network00120'
    network_description = 'Network Description'
    located_in_cloud = True
    owners = UserFactory.build()

    class Meta:
        model = Network


class ComputeResourceFactory(DjangoModelFactory):
    network = NetworkFactory.build()
    resource_name = 'Resource Name'
    portable = True
    local_ipv4_address = '18.20.12.30'
    local_ipv6_address = '17.96.15.12'
    external_ipv4_address = '17.96.85.14'
    external_ipv6_address = '17.36.45.25'
    powered_on_utc = fake.date_object(end_datetime=None)
    uptime = '17.00'
    last_seen = fake.date_object(end_datetime=None)
    description = 'description'

    class Meta:
        model = ComputeResource
