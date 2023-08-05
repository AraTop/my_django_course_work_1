from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
NULLABLE = {'null':True, 'blank':True}

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Customer_Service(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, verbose_name='Email', unique=True)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    password = models.CharField(max_length=128, default='')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} {self.last_name} {self.first_name} ' 

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'
        ordering = ('first_name',)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class Settings(models.Model):
    mailing_time = models.TimeField(verbose_name='Время рассылки')
    periodicity = models.CharField(max_length=100, verbose_name='Периодичность')
    mailing_status = models.CharField(max_length=100, verbose_name='Cтатус рассылки')
    client = models.ForeignKey(Customer_Service, on_delete=models.CASCADE, related_name='settings')
   
    def __str__(self):
        return f'{self.mailing_time} {self.periodicity} {self.mailing_status}' 
   
    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
        ordering = ('mailing_time',)

class Message_to_Send(models.Model):
    letter_subject = models.CharField(max_length=200, verbose_name='Тема письма')
    letter_body = models.TextField(verbose_name='Тело письма')
    settings = models.ForeignKey(Settings, on_delete=models.CASCADE, related_name='message_to_send')
   
    def __str__(self):
        return f'{self.letter_subject} {self.letter_body} {self.settings}' 
   
    class Meta:
        verbose_name = 'Cообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('letter_subject',)

class Mailing_Logs(models.Model):
    date_and_time_of_last_attempt = models.DateTimeField(verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=100, verbose_name='Статус попытки')
    mail_server_response = models.CharField(max_length=100, verbose_name='Ответ почтового сервера')
    settings = models.ForeignKey(Settings, on_delete=models.CASCADE, related_name='mailing_logs')
   
    def __str__(self):
        return f'{self.date_and_time_of_last_attempt} {self.attempt_status} {self.settings}' 
   
    class Meta:
        verbose_name = 'Журнал рассылок'
        verbose_name_plural = 'Журналы рассылок'
        ordering = ('date_and_time_of_last_attempt',)
