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

admin.site.register(ComponentMeasurementUnit)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(StorageUnit)
admin.site.register(StorageBin)
admin.site.register(Component)
admin.site.register(User)
admin.site.register(Borrow)
