from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class NimOrEmailBackend(BaseBackend):
    Usermodel = get_user_model()
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username.isdigit():
            try:
                user = self.Usermodel.objects.get(nim=username)
            except self.Usermodel.DoesNotExist:
                return None
        else:
            try:
                user = self.Usermodel.objects.get(email=username)
            except self.Usermodel.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None