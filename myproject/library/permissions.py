from rest_framework import permissions
from .models import Employer, Client


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and Employer.objects.filter(user=request.user).exists()


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and Client.objects.filter(user=request.user).exists()
