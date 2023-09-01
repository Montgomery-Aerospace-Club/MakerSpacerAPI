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
    Borrow,
)
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "user_id", "email", "password"]


class UserStudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "user_id", "email"]


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
        fields = ["url", "name", "short_code", "room"]


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


class ComponentMeasurementUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentMeasurementUnit
        fields = ["url", "unit_name", "unit_description"]


class ComponentPostSerializer(serializers.HyperlinkedModelSerializer):
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
            "description",
        ]


class ComponentGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = [
            "url",
            "unique_id",
            "name",
            "sku",
            "mpn",
            "upc",
            "storage_bin",
            "measurement_unit",
            "qty",
            "description",
        ]

        depth = 5


class BorrowPostSerializer(serializers.HyperlinkedModelSerializer):
    def update(self, instance, validated_data):
        instance.qty = validated_data.get("qty", instance.qty)
        instance.borrow_in_progress = validated_data.get(
            "borrow_in_progress", instance.borrow_in_progress
        )
        instance.timestamp_check_in = validated_data.get(
            "timestamp_check_in", instance.timestamp_check_in
        )
        return instance

    class Meta:
        model = Borrow
        fields = [
            "url",
            "qty",
            "person_who_borrowed",
            "timestamp_check_out",
            "timestamp_check_in",
            "borrow_in_progress",
            "component",
        ]


class BorrowGetSerializer(serializers.HyperlinkedModelSerializer):
    person_who_borrowed = UserStudentSerializer()

    class Meta:
        model = Borrow
        fields = [
            "url",
            "qty",
            "person_who_borrowed",
            "timestamp_check_out",
            "timestamp_check_in",
            "borrow_in_progress",
            "component",
        ]
        depth = 7

    # def update(self, instance, validated_data):
    #     # Update the Foo instance
    #     instance.person_who_checked_out = validated_data["person_who_checked_out"]
    #     instance.save()
    #     return instance

    # depth = 10
