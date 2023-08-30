from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'null':True, 'blank':True}

class User(AbstractUser):
   username = None
   email = models.EmailField(unique=True, verbose_name='Почта')

   first_name = models.CharField(max_length=150, verbose_name='Имя')
   last_name = models.CharField(max_length=150, verbose_name='Фамилия')
   surname = models.CharField(max_length=200, verbose_name='Отчество', **NULLABLE)
   comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

   email_confirmation_token = models.CharField(max_length=255, **NULLABLE)
   is_email_verified = models.BooleanField(default=False)
   
   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = []
