from django.contrib.auth.backends import ModelBackend
from .models import User

class NIMAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"🔍 Backend called with username: {username}")
        try:
            user = User.objects.get(nim=username)
            print(f"✓ Found user: {user.email}")
            if user.check_password(password):
                print(f"✓ Password correct!")
                return user
            else:
                print(f"✗ Password incorrect!")

                print(f"✗ Password incorrect for user with NIM: {username}")
                print(f"🔍 User password field starts with: {user.password[:20]}")
        except User.DoesNotExist:
            print(f"✗ No user with NIM: {username}")
            return None
        return None

