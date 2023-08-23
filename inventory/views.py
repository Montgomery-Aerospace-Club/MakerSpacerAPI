from django.shortcuts import render
from rest_framework import response, status

# Create your views here.
from .models import (
    Building,
    Room,
    StorageUnit,
    StorageBin,
    Component,
    ComponentMeasurementUnit,
    User,
)
from rest_framework import viewsets, permissions, filters
from inventory.serializers import (
    BuildingSerializer,
    RoomSerializer,
    StorageUnitSerializer,
    StorageBinSerializer,
    ComponentSerializer,
    ComponentMeasurementUnitSerializer,
    UserSerializer,
)


def index(request):
    return render(request, "index.html")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("name")
    search_fields = ["user_id", "name"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows building to be viewed or edited.
    """

    queryset = Building.objects.all().order_by("name")
    search_fields = ["name", "address", "postcode"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Room.objects.all()
    search_fields = ["name"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class StorageUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = StorageUnit.objects.all()
    search_fields = ["name"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = StorageUnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class StorageBinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = StorageBin.objects.all()
    search_fields = ["name", "short_code"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = StorageBinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class ComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Component.objects.all()
    search_fields = [
        "name",
        "checked_out",
        "description",
        "person_who_checked_out__user_id",
    ]
    filter_backends = (filters.SearchFilter,)
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class ComponentMeasurementUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = ComponentMeasurementUnit.objects.all()
    serializer_class = ComponentMeasurementUnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)
