from datetime import datetime, timedelta
import time
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
         else:
            return 'Настройка: is_time_to_send не подтвердилась'

      except Settings.DoesNotExist:
         # Настройки не найдены
         pass

   def is_time_to_send(self, settings, current_time):
      """ Проверка, что текущее время соответствует времени рассылки и другим условиям """

      if settings.mailing_time > current_time:
         return True
      
      elif current_time > settings.mailing_time:
         return True
      
      return False

   def stop_send_message(self, user_stoping):
      if user_stoping == 'Stop':
         return True
      else:
         return False

   def constant_sending_cycle(self, settings):
      while True:
         if self.stop_send_message(settings):
            break
         else:
            self.process_dispatch(settings)

            if settings.periodicity == "раз в день":
               wait_interval = timedelta(days=1)

            elif settings.periodicity == "раз в неделю":
               wait_interval = timedelta(weeks=1)

            elif settings.periodicity == "раз в месяц":
               wait_interval = self.calculate_next_monthly_interval()

            time.sleep(wait_interval.total_seconds())

   def waiting_for_the_right_time(self, settings):
      """Ждем время рассылки в пределах одного дня"""
      now = timezone.now()
        
      # Определите время, в которое должна произойти следующая рассылка
      next_mailing_time = settings.mailing_time
      print(settings.mailing_time)
        
      # Вычислите, сколько времени осталось до следующей рассылки
      time_to_wait = (next_mailing_time - now).total_seconds()
      print(time_to_wait)
      if time_to_wait > 0:
         time.sleep(time_to_wait)
   
      return True 

   def calculate_next_monthly_interval(self):
      """Ждем время рассылки в пределах одного месяца"""
      # Определяем интервал времени до следующей рассылки
      now = timezone.now()
      next_month = now.month + 1
      next_year = now.year

      if next_month > 12:
         next_month = 1
         next_year += 1

      next_month_start = now.replace(year=next_year, month=next_month, day=1, hour=0, minute=0, second=0, microsecond=0)
      interval = next_month_start - now
      return interval            

   def send_message(self, message, user, settings):
      e = None 

      try:
            self.waiting_for_the_right_time(settings)

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