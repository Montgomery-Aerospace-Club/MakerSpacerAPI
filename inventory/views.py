from django.shortcuts import render
from rest_framework import response, status


# Create your views here.
from .models import (
    Borrow,
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
    BorrowSerializer,
    BuildingSerializer,
    RoomSerializer,
    StorageUnitSerializer,
    StorageBinSerializer,
    ComponentSerializer,
    ComponentMeasurementUnitSerializer,
    UserSerializer,
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action


def index(request):
    return render(request, "index.html")


class AuthReadOnlyPermission(permissions.BasePermission):
    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:  # Check if the user is an admin
                return True
            return view.action in ["list", "retrieve"]  # Allow read-only actions
        return False


class EveryoneReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:  # Check if the user is an admin
                return True
            return view.action in ["list", "retrieve"]  # Allow read-only actions
        return view.action in ["list", "retrieve"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["=user_id", "=email", "=username"]
    filter_backends = (filters.SearchFilter,)
    permission_classes = [AuthReadOnlyPermission]

    @action(methods=["post"], detail=False, permission_classes=[permissions.AllowAny])
    def register(self, request, *args, **kwargs):
        # This logic was taken from the `create` on `ModelViewSet`. Alter as needed.
        # print(request.data)
        # return Response(status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userPass = request.data.get("password", None)
        user_id = request.data["user_id"]
        username = request.data["username"]
        email = request.data["email"]
        if userPass:
            user = User.objects.create_user(
                username=username, email=email, password=userPass, user_id=user_id
            )
            user.save()

        else:
            return Response(
                {"password": ["This field may not be empty"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # self.perform_create(serializer)
        # serializer.save()
        # headers = self.get_success_headers(serializer.data)
        return Response({}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_202_ACCEPTED)


class UserLogIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "id": user.pk,
                "username": user.username,
                "user_id": user.user_id,
                "email": user.email,
            }
        )


class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows building to be viewed or edited.
    """

    queryset = Building.objects.all().order_by("name")
    search_fields = ["name", "address", "postcode"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = BuildingSerializer
    permission_classes = [EveryoneReadOnlyPermission]


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Room.objects.all()
    search_fields = ["name"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = RoomSerializer
    permission_classes = [EveryoneReadOnlyPermission]


class StorageUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = StorageUnit.objects.all()
    search_fields = ["name"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = StorageUnitSerializer
    permission_classes = [EveryoneReadOnlyPermission]


class StorageBinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = StorageBin.objects.all()
    search_fields = ["name", "short_code"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = StorageBinSerializer
    permission_classes = [EveryoneReadOnlyPermission]


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    search_fields = [
        "=timestamp_check_out",
        "person_who_borrowed__username",
        "=person_who_borrowed__user_id",
        "=person_who_borrowed__email",
        "=borrow_in_progress",  # boolean 1 and 0's
        "component__name",
        "component__description",
    ]

    filter_backends = (filters.SearchFilter,)
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Component.objects.all()
    search_fields = [
        "name",
        "description",
    ]

    filter_backends = (filters.SearchFilter,)
    serializer_class = ComponentSerializer
    permission_classes = [EveryoneReadOnlyPermission]


class ComponentMeasurementUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = ComponentMeasurementUnit.objects.all()
    serializer_class = ComponentMeasurementUnitSerializer
    permission_classes = [EveryoneReadOnlyPermission]
