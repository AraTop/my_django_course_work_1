from django.contrib import admin
from service.models import Customer_Service, Settings, Message_to_Send, Mailing_Logs

@admin.register(Customer_Service)
class Customer_ServiceAdmin(admin.ModelAdmin):
   list_display = ('email', 'last_name', 'first_name', 'surname', 'comment', 'access_token', 'refresh_token')

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
   list_display = ('mailing_time', 'periodicity', 'mailing_status', 'client')

@admin.register(Message_to_Send)
class Message_to_SendAdmin(admin.ModelAdmin):
   list_display = ('letter_subject', 'letter_body', 'settings')

@admin.register(Mailing_Logs)
class Mailing_LogsAdmin(admin.ModelAdmin):
   list_display = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')