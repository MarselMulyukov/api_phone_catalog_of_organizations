from django.db.models import Q
from django.utils.functional import empty
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins
from rest_framework.response import Response
from rest_framework_word_filter import FullWordSearchFilter


from .models import Company, Worker
from .serializers import CompanyListSerializer, SearchSerializer, WorkerSerializer


class MySearchView(generics.ListAPIView):
    queryset = Company.objects.all()
    def list(self, request, *args, **kwargs):
        companies = self.get_queryset()
        context = {}
        if 'q' in request.query_params:
            q = request.query_params['q']
            for s in companies:
                s.filtered_workers = s.workers.filter(Q(name__icontains=q) | Q(work_phone__icontains=q)).order_by('name')[:5]
            context['filtered']=True
        ser = SearchSerializer(data=companies, many=True, context=context)
        ser.is_valid()
        return Response(ser.data)


class WorkersUpdateDestroyView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
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
