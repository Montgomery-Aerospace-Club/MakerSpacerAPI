from django.urls import path

from inventory import views


urlpatterns = [
    path("", views.index, name="index"),
    path("buildings/", views.BuildingListView.as_view(), name="buildings"),
    path(
        "buildings/<int:pk>", views.BuildingDetailView.as_view(), name="building-detail"
    ),
]
