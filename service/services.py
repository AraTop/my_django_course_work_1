from datetime import datetime
from django.utils import timezone
from users.models import User
from .models import Settings, Message_to_Send, Mailing_Logs
from django.core.mail import send_mail
from project import settings as setting
class MailingService:

   def process_dispatch(self, settings_id):
      """Нахождение: settings, current_time. Раличные проверки, """
      try:
         settings = Settings.objects.get(pk=settings_id)
         current_time = datetime.now().time()
   
         if self.is_time_to_send(settings, current_time):
            if settings.mailing_status == "создана":
               settings.mailing_status = "запущена"
               settings.save()

            if settings.mailing_status == "запущена":
               settings_objects = Settings.objects.all()
               clients = settings_objects.values_list('client', flat=True)
               message = Message_to_Send.objects.filter(settings=settings).first()

               if message:
                  for client in clients:
                     user = User.objects.get(id=client)
                     self.send_message(message, user, settings)
               else:
                  return 'No message'

            if settings.mailing_status == "завершена":
               pass

      except Settings.DoesNotExist:
         # Настройки не найдены
         pass

   def is_time_to_send(self, settings, current_time):
      """ Проверка, что текущее время соответствует времени рассылки и другим условиям """

      if settings.mailing_time > current_time:
         self.waiting_for_the_right_time(settings)
         return True
      
      elif current_time > settings.mailing_time:
         self.waiting_for_the_right_time(settings)
         return True
      
      return False

   def waiting_for_the_right_time(self, settings):
      pass

   def get_last_sent_time(self, settings):
      try:
         last_log = Mailing_Logs.objects.filter(settings=settings, attempt_status="Success").order_by('date_and_time_of_last_attempt').first()
         if last_log:
            return last_log.date_and_time_of_last_attempt
      except Mailing_Logs.DoesNotExist:
         pass

      return None

   def send_message(self, message, user, settings):
      e = None 

      try:
         send_mail(
         subject=message.letter_subject,
         message=message.letter_body,
         from_email=setting.EMAIL_HOST_USER,
         recipient_list=[user.email]
         )

      except Exception as error:
         e = error
         return e

      finally:
         Mailing_Logs.objects.create(date_and_time_of_last_attempt=timezone.now(),
         attempt_status="Success" if not e else "Error",
         mail_server_response=str(e) if e else "Success",
         settings=settings)