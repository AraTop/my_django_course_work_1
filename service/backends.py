from django.contrib.auth.backends import BaseBackend
from .models import Customer_Service  

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Customer_Service.objects.get(email=email) 
            if user.check_password(password):
                return user
        except Customer_Service.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error in EmailBackend: {e}")
            return None
