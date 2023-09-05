from django.contrib import admin

# Register your models here.
from .models import (
    ComponentMeasurementUnit,
    Building,
    Room,
    StorageUnit,
    StorageBin,
    Component,
    User,
    Borrow,
)

from import_export.admin import ExportActionMixin


class BuildingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "address", "postcode")


class RoomAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "short_code", "building")


class StorageUnitAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "short_code", "room")


class StorageBinAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "short_code", "unit_row", "unit_column", "storage_unit")


class ComponentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "mpn",
        "upc",
        # "storage_bin",
        "measurement_unit",
        "qty",
        "description",
        "barcode",
    )


class BorrowAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "qty",
        "person_who_borrowed",
        "timestamp_check_out",
        "timestamp_check_in",
        "borrow_in_progress",
        "component",
    )


admin.site.register(ComponentMeasurementUnit)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(StorageUnit, StorageUnitAdmin)
admin.site.register(StorageBin, StorageBinAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(User)
admin.site.register(Borrow, BorrowAdmin)
