from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Company, Worker, User


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name", "position", "private_phone", "work_phone", "fax")
        model = Worker

    def validate(self, attrs):
        name = attrs['name']
        private_phone = attrs['private_phone']
        work_phone = attrs['work_phone']
        fax = attrs['fax']
        company_id = self.context['view'].kwargs['company_id']
        worker = Worker.objects.filter(private_phone=private_phone)
        if worker and private_phone:
            raise ValidationError('Личный номер телефона не уникален')
        worker = Worker.objects.filter(name=name, company_id=company_id)
        if worker:
            raise ValidationError('В этой организации уже записан данный работник')
        if not (private_phone or work_phone or fax):
            raise ValidationError('Хотя бы один номер телефона или факс должны быть заполнены')
        return attrs


class CompanySerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(read_only=True, many=True)

    class Meta:
        fields = ("title", "info", "address", "workers")
        model = Company


class RedactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)


class RedactorOfCompanySerializer(serializers.ModelSerializer):
    redactor = RedactorSerializer(many=True)
    class Meta:
        model = Company
        fields = ("redactor",)


class AdmittedCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model =Company
        fields = ("title",)
