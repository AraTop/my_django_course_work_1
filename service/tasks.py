from django.core.mail import send_mail
from project import settings
from service.models import Mailing_Logs, Message_to_Send, Settings
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from celery import shared_task

@shared_task
def send_mailing_task(mailing):
   settings_objects = Settings.objects.all()
   recipients = settings_objects.values_list('client', flat=True)
   print(recipients)
   subject = mailing.letter_subject
   message = mailing.letter_body

   for recipient in recipients:
      recipient_email = recipient.email

      try:
         send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email])
         
         log = Mailing_Logs(
            date_and_time_of_last_attempt=timezone.now(),
            attempt_status="Success",
            mail_server_response="Success",
            settings=Settings.object.filter(client_id=recipient.pk))
         log.save()

      except Exception as e:
         log = Mailing_Logs(
            date_and_time_of_last_attempt=timezone.now(),
            attempt_status="Error",
            mail_server_response=e,
            settings=Settings.object.filter(client_id=recipient.pk))
         log.save()

   mailing.save()

@shared_task
def start_mailings():
   """
   Функция для запуска отложенных рассылок.
   Эта функция будет вызываться периодически по расписанию и отправлять рассылки,
   которые готовы к отправке на текущий момент.
   Периодичность отправки рассылок зависит от настроек каждой рассылки.
   """
   
   current_time = timezone.now()
   # Фильтруем объекты Mailing, чтобы найти те, которые имеют статус Mailing.STATUS_CREATED
   # или Mailing.STATUS_STARTED и у которых время рассылки меньше или равно текущему времени.
   settings_objects = Settings.objects.filter(Q(mailing_status="создана") | Q(mailing_status="запущена"), mailing_time_date__lte=current_time)

   scheduled_mailings = Message_to_Send.objects.filter(settings__in=settings_objects)

   for mailing in scheduled_mailings:
      setting = mailing.settings
      setting.mailing_status = "запущена"
      print(setting.mailing_status)
      setting.save()
      send_mailing_task.delay(mailing)


      if setting.periodicity == "раз в день":
         setting.mailing_time_date += timedelta(days=1)
      elif setting.periodicity == "раз в неделю":
         setting.mailing_time_date += timedelta(weeks=1)
      elif setting.periodicity == "раз в месяц":
         setting.mailing_time_date += relativedelta(months=1)

      if setting.mailing_time_date.day > 28:
         setting.mailing_time_date = mailing.mailing_time_date.replace(day=1)
         setting.mailing_time_date += relativedelta(day=31)

      setting.save()