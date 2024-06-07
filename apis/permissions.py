from rest_framework.permissions import BasePermission
from .models import ApiKey


class HasAPIKey(BasePermission):

    def has_permission(self, request, view):
        try:
            key = request.headers['Authorization'].split()[1]
        except KeyError:
            return False

        try:
            k = ApiKey.objects.get(key=key)
            print(k.email)
        except ApiKey.DoesNotExist:
            return False

        return True
