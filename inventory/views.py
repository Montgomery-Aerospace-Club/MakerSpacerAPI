import itertools
import json

from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import response, status
from django.utils import timezone

from inventory.perms import (
    AuthReadOnlyPermission,
    AuthorizedUserCanOnlyReadAndUpdate,
    EveryoneReadOnlyPermission,
)

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
from django_filters import rest_framework as filters_rest
from inventory.serializers import (
    BorrowGetSerializer,
    BorrowPostSerializer,
    BuildingSerializer,
    RoomSerializer,
    StorageUnitSerializer,
    StorageBinSerializer,
    ComponentGetSerializer,
    ComponentMeasurementUnitSerializer,
    UserSerializer,
    ComponentPostSerializer,
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from django.views import generic
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .encoders import UUIDEncoder
from django.db.models import Q


def index(request):
    return render(request, "index.html")


def dashboard(request):
    return render(request, "dashboard/dashboard.html")


def login_form(request):
    return render(request, "app/login.html")


def logoutView(request):
    logout(request)
    return redirect("dashboard")


def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        request.session["token"] = ""
        if user is not None and user.is_active:
            auth.login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            request.session["token"] = token.key
            request.session.set_expiry = 0

            return redirect("dashboard")

        else:
            messages.info(request, "Invalid username or password")
            return redirect("login_page")


class BuildingListView(generic.ListView):
    model = Building
    context_object_name = "building_list"
    # query set also works
    #  def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BuildingListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class BuildingDetailView(generic.DetailView):
    model = Building


class RoomListView(generic.ListView):
    model = Room


class RoomDetailView(generic.DetailView):
    model = Room


class StorageUnitListView(generic.ListView):
    model = StorageUnit
    context_object_name = "unit_list"


class StorageUnitDetailView(generic.DetailView):
    model = StorageUnit
    context_object_name = "unit"


class StorageBinListView(generic.ListView):
    model = StorageBin
    context_object_name = "bin_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(StorageBinListView, self).get_context_data(**kwargs)
        q = self.request.GET.get("search")
        context["search"] = q
        return context

    def get_queryset(self):
        queryset = StorageBin.objects.all().order_by("id")

        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            if search != "None":
                queryset = StorageBin.objects.filter(
                    Q(name__icontains=search) | Q(short_code__icontains=search)
                ).order_by("id")

        return queryset


class StorageBinDetailView(generic.DetailView):
    model = StorageBin
    context_object_name = "bin"


class ComponentListView(generic.ListView):
    model = Component
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(ComponentListView, self).get_context_data(**kwargs)
        q = self.request.GET.get("search")
        context["search"] = q
        return context

    def get_queryset(self):
        queryset = Component.objects.all().order_by("name")

        pk = None
        if self.request.GET.get("id"):
            pk = self.request.GET.get("name")
            print(pk)
            try:
                pk = int(pk)
            except ValueError:
                pk = None
            if pk is not None:
                queryset = Component.objects.filter(Q(id=pk)).order_by("name")
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            if search != "None":
                queryset = Component.objects.filter(
                    Q(description__icontains=search) | Q(name__icontains=search)
                ).order_by("name")

        return queryset


class ComponentDetailView(generic.DetailView):
    model = Component


class BorrowListView(generic.ListView):
    model = Borrow
    paginate_by = 15
    """
    search_fields = [
        "person_who_borrowed__username",
        "component__name",
        "component__description",
        "timestamp_check_out",
    ]
    filterset_fields = [
        "component__id",
        "borrow_in_progress",
        "person_who_borrowed__user_id",
        "person_who_borrowed__email",
    ]
    ordering_fields = ["borrow_in_progress"]
    """

    def get_context_data(self, **kwargs):
        context = super(BorrowListView, self).get_context_data(**kwargs)
        q = self.request.GET.get("search")
        context["search"] = q
        comp = ""
        if self.request.GET.get("component"):
            comp = Component.objects.get(pk=self.request.GET.get("component"))
        context["comp"] = comp

        user = ""
        if self.request.GET.get("user"):
            user = User.objects.get(pk=self.request.GET.get("user"))
        context["user"] = user

        status_e = self.request.GET.get("status")
        context["status"] = status_e

        context["users"] = User.objects.all()
        context["components"] = Component.objects.all().distinct()
        return context

    def get_queryset(self):
        queryset = Borrow.objects.all().order_by("-id")
        searchOrfilters = False
        qs = Borrow.objects.all().order_by("-id")

        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            if search != "None":
                qs = Borrow.objects.filter(
                    Q(component__description__icontains=search)
                    | Q(component__name__icontains=search)
                ).order_by("-id")
                searchOrfilters = True

        if self.request.GET.get("status"):
            stat = self.request.GET.get("status")
            if stat == "True":
                qs = Borrow.objects.filter(borrow_in_progress=True).order_by(
                    "component__name"
                )
            elif stat == "False":
                qs = Borrow.objects.filter(borrow_in_progress=False).order_by(
                    "component__name"
                )
            searchOrfilters = True

        if self.request.GET.get("component"):
            compID = self.request.GET.get("component")
            if self.request.GET.get("status"):
                stat = self.request.GET.get("status")
                if stat == "True":
                    qs = Borrow.objects.filter(
                        Q(borrow_in_progress=True) & Q(component__pk=compID)
                    ).order_by("component__name")
                elif stat == "False":
                    qs = Borrow.objects.filter(
                        Q(borrow_in_progress=False) & Q(component__pk=compID)
                    ).order_by("component__name")
            else:
                qs = Borrow.objects.filter(component__pk=compID).order_by(
                    "-borrow_in_progress"
                )

            searchOrfilters = True

        if self.request.GET.get("user"):
            userID = self.request.GET.get("user")
            if self.request.GET.get("status"):
                stat = self.request.GET.get("status")
                if stat == "True":
                    qs = Borrow.objects.filter(
                        Q(borrow_in_progress=True) & Q(person_who_borrowed__pk=userID)
                    ).order_by("component__name")
                elif stat == "False":
                    qs = Borrow.objects.filter(
                        Q(borrow_in_progress=False) & Q(person_who_borrowed__pk=userID)
                    ).order_by("component__name")
            else:
                qs = Borrow.objects.filter(person_who_borrowed__pk=userID).order_by(
                    "-borrow_in_progress"
                )

            searchOrfilters = True

        if self.request.GET.get("user") and self.request.GET.get("component"):
            compID = self.request.GET.get("component")
            userID = self.request.GET.get("user")
            if self.request.GET.get("status"):
                stat = self.request.GET.get("status")
                if stat == "True":
                    qs = Borrow.objects.filter(
                        Q(borrow_in_progress=True)
                        & Q(person_who_borrowed__pk=userID)
                        & Q(component__pk=compID)
                    ).order_by("component__name")
                elif stat == "False":
                    qs = Borrow.objects.filter(
                        Q(borrow_in_progress=False)
                        & Q(person_who_borrowed__pk=userID)
                        & Q(component__pk=compID)
                    ).order_by("component__name")
            else:
                qs = Borrow.objects.filter(
                    Q(person_who_borrowed__pk=userID) & Q(component__pk=compID)
                ).order_by("-borrow_in_progress")

            searchOrfilters = True

        if searchOrfilters:
            return qs
        return queryset


class BorrowDetailView(generic.DetailView):
    model = Borrow


class ComponentMeasurementUnitDetailView(generic.DetailView):
    model = ComponentMeasurementUnit
    context_object_name = "unit"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["=user_id", "=email", "username"]
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
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                "isadmin": user.is_staff,
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
    search_fields = ["name", "short_code"]
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
        "person_who_borrowed__username",
        "component__name",
        "component__description",
        "timestamp_check_out",
    ]
    filterset_fields = [
        "component__id",
        "borrow_in_progress",
        "person_who_borrowed__user_id",
        "person_who_borrowed__email",
    ]
    ordering_fields = ["borrow_in_progress"]

    filter_backends = [
        filters.SearchFilter,
        filters_rest.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    # serializer_class = BorrowSerializer
    permission_classes = [AuthorizedUserCanOnlyReadAndUpdate]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qty = serializer.validated_data["qty"]
        comp = serializer.validated_data["component"]
        serializer.validated_data["borrow_in_progress"] = True

        if comp.qty - qty < 0:
            return Response(
                {
                    "details": [
                        f"You cannot overborrow the item: {comp.name}",
                        f"Component Quantity: {comp.qty}",
                        f"Asked Quantity: {qty}",
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            # TODO: create qty component returns

        comp_db = Component.objects.get(pk=comp.pk)
        comp_db.qty -= qty
        comp_db.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        qty = serializer.validated_data.get("qty", None)
        comp = instance.component

        if instance.person_who_borrowed.pk != request.user.pk and (
            not request.user.is_staff
        ):
            return Response(
                {"details": ["You cannot modify someone else's borrow!"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # checks if we are udating the borrow amount or not and checks if the borrow is in progress to prevent people from changing old records
        if not instance.borrow_in_progress:
            return Response(
                {
                    "details": [
                        "Cannot modify already returned component's borrow instance",
                        "This is the incorrect form if you are trying to borrow the item you inputed",
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if qty:
            if comp.qty + instance.qty - qty < 0:
                return Response(
                    {
                        "details": [
                            f"You cannot overborrow the item: {comp.name}",
                            f"Component Quantity Available (amount + old qty): {comp.qty + instance.qty}",
                            f"Asked Quantity (new qty): {qty}",
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.validated_data["timestamp_check_in"] = None
            serializer.validated_data["borrow_in_progress"] = True

            comp.qty = comp.qty + instance.qty - qty
            comp.save()

            serializer.save()

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

        else:  # looks like we are not updating the qty, lets take a look at the other two fields
            inProgress = serializer.validated_data.get("borrow_in_progress", False)
            if inProgress and (not request.user.is_staff):
                return Response(
                    {
                        "details": [
                            f"Cannot modify borrow_in_progress field from {instance.borrow_in_progress} to True",
                            "This essentially means that you are 'reviving' this borrow which is illegal",
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # this runs if inProgress field in the request body is false, meaning we are "closing" or "concluding" the borrow
            # this code below is to start the return "process"
            if serializer.validated_data.get(
                "timestamp_check_in", instance.timestamp_check_in
            ) is None and (not request.user.is_staff):
                return Response(
                    {
                        "details": [
                            "If you are closing this borrow, you need to add a timestamp_check_in field",
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            comp.qty += instance.qty
            comp.save()

            instance.borrow_in_progress = serializer.validated_data.get(
                "borrow_in_progress", instance.borrow_in_progress
            )
            instance.timestamp_check_in = serializer.validated_data.get(
                "timestamp_check_in", instance.timestamp_check_in
            )
            instance.save()

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response({})

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BorrowPostSerializer
        return BorrowGetSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Component.objects.all()
    search_fields = ["name", "description", "=unique_id", "=id"]
    ordering_fields = ["name"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # serializer_class = ComponentGetSerializer
    permission_classes = [EveryoneReadOnlyPermission]

    def get_serializer_class(self):
        if self.action == "create":
            return ComponentPostSerializer
        return ComponentGetSerializer


class ComponentMeasurementUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = ComponentMeasurementUnit.objects.all()
    serializer_class = ComponentMeasurementUnitSerializer
    permission_classes = [EveryoneReadOnlyPermission]


def borrowComponent(request: HttpRequest):
    comps = Component.objects.all()
    if not request.user.is_authenticated:
        messages.error(
            request, "You need to be logged in in order to borrow makerspace items!"
        )
        messages.info(
            request,
            "You are currently not logged in! Login at /login/ or go to dashboard",
        )

    return render(
        request,
        "dashboard/borrow.html",
        {
            "components": comps,
            "userurl": f"http://127.0.0.1:8000/rest/users/{request.user.pk}/",
            "user": request.user,
        },
    )


def createBorrowFromForm(request: HttpRequest):
    if request.POST:
        if request.user.is_authenticated:
            evl = BorrowViewSet.as_view({"post": "create"})(request)
            data = evl.data
            # print(data)
            status_code = evl.status_code
            if status_code == 400:
                if "details" in data:
                    errors = data["details"]
                    for error in errors:
                        messages.error(request, error)
                else:
                    for key in data:
                        errorstr = f"{key}: {data[key][0].title()}"
                        messages.error(request, errorstr)
            else:
                # print("success")
                messages.success(request, "Created borrow for component!")
                messages.success(
                    request,
                    f"Copy and paste this link to view it: {data['url'].replace('/rest', '')}",
                )

        else:
            messages.error(request, "You are not logged in!")
            messages.info(request, "Login at /login/")

    return redirect("createborrowpage")
