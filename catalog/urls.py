from django.urls import path

from . import views

urlpatterns = [
    path("destinations/", views.DestinationListView.as_view(), name="destination-list"),
    path("destinations/<slug:slug>/", views.DestinationDetailView.as_view(), name="destination-detail"),
    path("packages/", views.SafariPackageListView.as_view(), name="package-list"),
    path("packages/<slug:slug>/", views.SafariPackageDetailView.as_view(), name="package-detail"),
]
