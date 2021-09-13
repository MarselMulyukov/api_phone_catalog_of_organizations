from typing import Iterable
from rest_framework import permissions
from .models import Company


class OnlyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    def has_permission(self, request, view):
        company = Company.objects.get(id=view.kwargs['company_id'])
        return request.user == company.author


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)


class IsOwnerOrRedactorOfCompanyOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.company.author
            or request.user in obj.company.redactor.all())

    def has_permission(self, request, view):
        company = Company.objects.get(id=view.kwargs['company_id'])
        redactors = [user for user in company.redactor.all()]
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == company.author
            or request.user in redactors)