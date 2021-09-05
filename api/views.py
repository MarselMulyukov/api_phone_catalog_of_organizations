from rest_framework import filters, generics

from .models import Company, Worker
from .serializers import CompanyListSerializer, WorkerSerializer


class WorkersUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkerSerializer
    def get_queryset(self):
        worker = Worker.objects.filter(company_id=self.kwargs['company_id'], pk=self.kwargs['pk'])
        return worker
    

class WorkersCreateListView(generics.ListCreateAPIView):
    serializer_class = WorkerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'position', 'work_phone']

    def get_queryset(self):
        workers = Worker.objects.filter(company_id=self.kwargs['company_id'])
        return workers
        
    def perform_create(self, serializer):
        return serializer.save(company_id=self.kwargs['company_id'])


class CompaniesView(generics.ListAPIView):
    queryset = Company.objects.all().order_by("title")
    serializer_class = CompanyListSerializer
