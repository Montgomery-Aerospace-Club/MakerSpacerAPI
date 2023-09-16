from django.urls import path

from inventory import views


urlpatterns = [
    # shared urls
    path("login/", views.login_form, name="login_page"),
    path("userLogin/", views.loginView, name="login"),
    # List and Detail views
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("buildings/", views.BuildingListView.as_view(), name="buildings"),
    path(
        "buildings/<int:pk>", views.BuildingDetailView.as_view(), name="building-detail"
    ),
    path("rooms/", views.RoomListView.as_view(), name="rooms"),
    path("rooms/<int:pk>", views.RoomDetailView.as_view(), name="room-detail"),
    path("units/", views.StorageUnitListView.as_view(), name="units"),
    path("units/<int:pk>", views.StorageUnitDetailView.as_view(), name="unit-detail"),
    path("bins/", views.StorageBinListView.as_view(), name="bins"),
    path("bins/<int:pk>", views.StorageBinDetailView.as_view(), name="bin-detail"),
    path("components/", views.ComponentListView.as_view(), name="components"),
    path(
        "components/<int:pk>",
        views.ComponentDetailView.as_view(),
        name="component-detail",
    ),
    path("borrows/", views.BorrowListView.as_view(), name="borrows"),
    path(
        "borrows/<int:pk>",
        views.BorrowDetailView.as_view(),
        name="borrow-detail",
    ),
    path(
        "compmeasurements/<int:pk>",
        views.ComponentMeasurementUnitDetailView.as_view(),
        name="compmeasurements-detail",
    ),
]
