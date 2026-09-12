from django.urls import path

from . import views

urlpatterns = [
    path("contact/", views.ContactEnquiryCreateView.as_view(), name="contact-create"),
    path("plan-my-trip/", views.TripEnquiryCreateView.as_view(), name="trip-create"),
]
