from re import S
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Company, Worker


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name", "position", "private_phone", "work_phone", "fax", "company")
        model = Worker
        validators = [UniqueTogetherValidator(
            queryset=Worker.objects.all(),
            fields=["name", "company"],
            message="That man exist"
        ),]


class WorkersSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('name', 'position', 'work_phone')


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(SearchSerializer, self).__init__(*args, **kwargs)
        filtered = self.context.get("filtered", None)
        if filtered is not None:
            wrkrs = WorkersSearchSerializer(
                source='filtered_workers', many=True)
        else:
            wrkrs = WorkersSearchSerializer(many=True)

        self.fields['workers'] = wrkrs

    

class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("title", "info", "address")
        model = Company
