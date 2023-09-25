from django.core.mail import send_mail
from project import settings
from service.models import Mailing_Logs, Message_to_Send, Settings
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

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
            recipient_list=[recipient_email],
            fail_silently=False,)
         
         log = Mailing_Logs(
            mailing=mailing,
            recipient=recipient,
            status=Mailing_Logs.STATUS_SUCCESSFUL,)
         log.save()

      except Exception as e:
         log = Mailing_Logs(
            mailing=mailing,
            recipient=recipient,
            status=Mailing_Logs.STATUS_FAILED, 
            error_message=str(e),)
         
         log.save()

   mailing.save()

def start_scheduled_mailings():
   """
   Функция для запуска отложенных рассылок.
   Эта функция будет вызываться периодически по расписанию и отправлять рассылки,
   которые готовы к отправке на текущий момент.
   Периодичность отправки рассылок зависит от настроек каждой рассылки.
   """
   
   current_time = timezone.now()
   # Фильтруем объекты Mailing, чтобы найти те, которые имеют статус Mailing.STATUS_CREATED
   # или Mailing.STATUS_STARTED и у которых время рассылки меньше или равно текущему времени.
   settings_objects = Settings.objects.filter(Q(mailing_status="создана") | Q(mailing_status="запущена"), mailing_time__lte=current_time)

   scheduled_mailings = Message_to_Send.objects.filter(settings__in=settings_objects)

   for mailing in scheduled_mailings:
      setting = mailing.settings
      setting.mailing_status = "запущена"
      print(setting.mailing_status)
      setting.save()
      send_mailing_task(mailing)


      if setting.periodicity == "раз в день":
         setting.mailing_time += timedelta(days=1)
      elif setting.periodicity == "раз в неделю":
         setting.mailing_time += timedelta(weeks=1)
      elif setting.periodicity == "раз в месяц":
         setting.mailing_time += relativedelta(months=1)

      if setting.mailing_time.day > 28:
         setting.mailing_time = mailing.mailing_time.replace(day=1)
         setting.mailing_time += relativedelta(day=31)

      setting.save()


scheduler = BackgroundScheduler()
scheduler.add_job(start_scheduled_mailings, CronTrigger(second='0'))
scheduler.start()
print("Scheduler started")