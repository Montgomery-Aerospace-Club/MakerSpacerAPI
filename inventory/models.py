import uuid

from django.db import models
from django.core.validators import MinValueValidator
from django_prometheus.models import ExportModelOperationsMixin
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser


from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import os

from django.urls import reverse


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    user_id = models.PositiveIntegerField(
        default=00000, validators=[MaxValueValidator(999999)], unique=True
    )

    def __str__(self):
        return self.username


class Building(ExportModelOperationsMixin("Building"), models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("building-website-detail", args=[str(self.id)])


class Room(ExportModelOperationsMixin("Room"), models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=5, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("room-website-detail", args=[str(self.id)])


class StorageUnit(ExportModelOperationsMixin("StorageUnit"), models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=5, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("unit-website-detail", args=[str(self.id)])


class StorageBin(ExportModelOperationsMixin("StorageBin"), models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=5, null=True, blank=True)
    unit_row = models.CharField(max_length=5, null=True, blank=True)
    unit_column = models.CharField(max_length=5, null=True, blank=True)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("bin-website-detail", args=[str(self.id)])


class ComponentMeasurementUnit(
    ExportModelOperationsMixin("ComponentMeasurementUnit"), models.Model
):
    unit_name = models.CharField(max_length=30)
    unit_description = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.unit_name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("compmeasurements-website-detail", args=[str(self.id)])


class Component(ExportModelOperationsMixin("Component"), models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    sku = models.CharField(max_length=100, default="", blank=True)
    mpn = models.CharField(max_length=100, default="", blank=True)
    upc = models.IntegerField(blank=True, null=True)
    storage_bin = models.ManyToManyField(StorageBin)
    measurement_unit = models.ForeignKey(
        ComponentMeasurementUnit, on_delete=models.CASCADE
    )
    qty = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(default="", blank=True)
    barcode = models.ImageField(
        upload_to="barcodes/", blank=True, default="barcodes/barcode.png"
    )

    def __str__(self):
        return self.name

    # TODO: Problem here! I need to like change it cuz when on the first save there is no pk, i need to use a different uuid variable like
    # short uuid or smth from a package.
    def save(self, *args, **kwargs):
        path = os.path.join(
            "media", "barcodes", f"{self.name}_{self.pk}.png".replace(" ", "_")
        )
        if not (os.path.isfile(path)):
            barclass = barcode.get_barcode_class("Code128")
            code = barclass(f"{self.pk}", writer=ImageWriter())
            buffer = BytesIO()
            code.write(buffer)

            self.barcode.save(f"{self.name}_{self.pk}.png", File(buffer), save=False)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("component-website-detail", args=[str(self.id)])


class Borrow(ExportModelOperationsMixin("Borrow"), models.Model):
    qty = models.IntegerField(validators=[MinValueValidator(1)])
    person_who_borrowed = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp_check_out = models.DateTimeField()
    timestamp_check_in = models.DateTimeField(null=True, blank=True)
    borrow_in_progress = models.BooleanField(default=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)

    class Meta:
        ordering = ["timestamp_check_out"]

    def __str__(self):
        return (
            f"Borrow - Amount: {self.qty} - Person: {self.person_who_borrowed.username}"
        )

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse("borrow-website-detail", args=[str(self.id)])
