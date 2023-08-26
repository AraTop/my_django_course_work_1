from service.models import Settings, Message_to_Send, Mailing_Logs 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from service.permissions import AuthorMessagePermissionsMixin, AuthorPermissionsMixin, ModeratorMessagePermissionsMixin, ModeratorPermissionsMixin
from users.models import User
from django.http import JsonResponse
from django.views import View
from .services import MailingService

@method_decorator(login_required, name='dispatch')
class SettingsCreateView(CreateView):
   model = Settings
   fields = ('mailing_time', 'periodicity', 'mailing_status', 'client')
   success_url = '/service/settings/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs) 
      settings_objects = User.objects.all()
      context['objects'] = settings_objects
      return context

@method_decorator(login_required, name='dispatch')
class SettingsDeleteView(AuthorPermissionsMixin, DeleteView):
   model = Settings
   success_url = '/service/settings/' 
   
@method_decorator(login_required, name='dispatch')
class SettingsListView(ListView):
   model = Settings

@method_decorator(login_required, name='dispatch')
class SettingsDetailView(ModeratorPermissionsMixin, DetailView):
   model = Settings

@method_decorator(login_required, name='dispatch')
class SettingsUpdateView(ModeratorPermissionsMixin, UpdateView):
   model = Settings
   fields = ('mailing_time', 'periodicity', 'mailing_status', 'client')
   success_url = '/service/settings/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = User.objects.all()
      context['objects'] = settings_objects
      return context
   
#--------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class Message_to_SendCreateView(CreateView):
   model = Message_to_Send
   fields = ('letter_subject', 'letter_body', 'settings')
   success_url = '/service/message/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.filter(client_id=self.request.user.id)
      context['objects'] = settings_objects
      return context
   
@method_decorator(login_required, name='dispatch')
class Message_to_SendDeleteView(AuthorMessagePermissionsMixin, DeleteView):
   model = Message_to_Send
   success_url = '/service/message/' 

@method_decorator(login_required, name='dispatch')
class Message_to_SendListView(ListView):
   model = Message_to_Send
   
@method_decorator(login_required, name='dispatch')
class Message_to_SendDetailView(ModeratorMessagePermissionsMixin, DetailView):
   model = Message_to_Send

@method_decorator(login_required, name='dispatch')
class Message_to_SendUpdateView(ModeratorMessagePermissionsMixin, UpdateView):
   model = Message_to_Send
   fields = ('letter_subject', 'letter_body', 'settings')
   success_url = '/service/message/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.filter(client_id=self.request.user.id)
      context['objects'] = settings_objects
      return context
   
#--------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class Mailing_LogsCreateView(ModeratorMessagePermissionsMixin, CreateView):
   model = Mailing_Logs
   fields = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')
   success_url = '/service/logs/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context

@method_decorator(login_required, name='dispatch')
class Mailing_LogsDeleteView(ModeratorMessagePermissionsMixin, DeleteView):
   model = Mailing_Logs
   success_url = '/service/logs/' 

@method_decorator(login_required, name='dispatch')
class Mailing_LogsListView(ListView):
   model = Mailing_Logs

@method_decorator(login_required, name='dispatch')
class Mailing_LogsDetailView(ModeratorMessagePermissionsMixin, DetailView):
   model = Mailing_Logs

@method_decorator(login_required, name='dispatch')
class Mailing_LogsUpdateView(ModeratorMessagePermissionsMixin, UpdateView):
   model = Mailing_Logs
   fields = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')
   success_url = '/service/logs/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context
#----------------------------------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class CreateDispatchView(View):

   def get(self, request, *args, **kwargs):
      user_id = request.user.id
      if user_id:
         settings = Settings.objects.filter(client_id=user_id).first()
         settings_id = settings.id
         mailing_service = MailingService()
         mailing_service.process_dispatch(settings_id)
         return JsonResponse({"message": "Dispatch processed successfully"}),
      else:
         return JsonResponse({"message": "Settings not found for this user"})