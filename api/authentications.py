from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class EmailAndPasswordAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        email = request.META.get('HTTP_EMAIL', None)
        password = request.META.get('HTTP_PASSWORD', None)
        if not email or not password:
            return None
        try:
            user = User.objects.get(email=email) # get the user
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist 

        return (user, None) # authentication successful