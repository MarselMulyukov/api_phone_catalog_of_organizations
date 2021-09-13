from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Company, Worker, User
from .permissions import IsOwnerOrReadOnly, IsOwnerOrRedactorOfCompanyOrReadOnly, OnlyOwner
from .serializers import AdmittedCompaniesSerializer, CompanySerializer, RedactorOfCompanySerializer, WorkerSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by("title")
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrReadOnly,]
    filter_backends = [filters.SearchFilter,]
    search_fields = ['title', 'workers__name', 'workers__work_phone', 'workers__private_phone']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    permission_classes = [IsOwnerOrRedactorOfCompanyOrReadOnly,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'position', 'work_phone', 'private_phone']

    def get_queryset(self):
        workers = Worker.objects.filter(company_id=self.kwargs['company_id']).order_by("name")
        return workers

    def perform_create(self, serializer):
        return serializer.save(company_id=self.kwargs['company_id'])


class RedactorView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    permission_classes = [OnlyOwner,]
    serializer_class = RedactorOfCompanySerializer
    
    def get_queryset(self):
        company = Company.objects.filter(id=self.kwargs['company_id'])
        return company
    
    def post(self, request, *args, **kwargs):
        company = Company.objects.get(id=self.kwargs['company_id'])
        new_redactor = get_object_or_404(User, email=request.data['email'])
        company.redactor.add(new_redactor)
        return Response({'detail': 'redactor was added'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        company = Company.objects.get(id=self.kwargs['company_id'])
        redactor_to_delete = get_object_or_404(User, email=request.data['email'])
        company.redactor.remove(redactor_to_delete)
        return Response({'detail': 'redactor was deleted'}, status=status.HTTP_204_NO_CONTENT)


class AdmittedCompaniesView(generics.ListAPIView):
    serializer_class = AdmittedCompaniesSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        me = self.request.user
        companies_to_edit = me.companies_to_edit.all()
        my_company = Company.objects.filter(author=me)
        companies_to_edit = companies_to_edit.union(my_company)
        return companies_to_edit
