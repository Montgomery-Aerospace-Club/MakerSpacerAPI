import os
from .utils import OctopartClient
from .models import (
    Building,
    Room,
    StorageUnit,
    StorageBin,
    Component,
    ComponentMeasurementUnit,
    User,
)
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "user_id", "email", "password"]


class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ["url", "name", "address", "postcode"]


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ["url", "name", "building"]


class StorageUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageUnit
        fields = ["url", "name", "room"]


class StorageBinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageBin
        fields = [
            "url",
            "name",
            "short_code",
            "unit_row",
            "unit_column",
            "storage_unit",
        ]


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = [
            "url",
            "name",
            "sku",
            "mpn",
            "upc",
            "storage_bin",
            "measurement_unit",
            "qty",
            "checked_out",
            "person_who_checked_out",
            "description",
        ]

    # def update(self, instance, validated_data):
    #     # Update the Foo instance
    #     instance.person_who_checked_out = validated_data["person_who_checked_out"]
    #     instance.save()
    #     return instance

    # depth = 10


class ComponentMeasurementUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentMeasurementUnit
        fields = ["url", "unit_name", "unit_description"]
