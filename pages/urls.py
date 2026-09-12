from django.urls import path

from . import views

urlpatterns = [
    path("faqs/", views.FAQListView.as_view(), name="faq-list"),
    path("<slug:slug>/", views.PageDetailView.as_view(), name="page-detail"),
]
