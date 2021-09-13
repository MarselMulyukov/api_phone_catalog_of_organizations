from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdmittedCompaniesView, CompanyViewSet, RedactorView, WorkerViewSet

router_v1 = DefaultRouter()
router_v1.register('companies', CompanyViewSet, basename='companies')
router_v1.register(r'companies/(?P<company_id>[^/.]+)/workers', WorkerViewSet, basename='workers')

urlpatterns = [
    path("v1/companies/admitted", AdmittedCompaniesView.as_view()),
    path("v1/companies/<int:company_id>/redactors", RedactorView.as_view()),
    path('v1/', include(router_v1.urls)),
]