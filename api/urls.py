from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompaniesView, WorkersCreateListView, WorkersUpdateDestroyView

urlpatterns = [
    path("v1/companies", CompaniesView.as_view()),
    path("v1/companies/<int:company_id>/workers", WorkersCreateListView.as_view()),
    path("v1/companies/<int:company_id>/workers/<int:pk>/", WorkersUpdateDestroyView.as_view()),
]