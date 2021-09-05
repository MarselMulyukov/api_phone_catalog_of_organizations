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
    

class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("title", "info", "address")
        model = Company
