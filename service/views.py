from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from service.models import Customer_Service, Settings, Message_to_Send, Mailing_Logs 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

class CustomerCreateView(CreateView):
   model = Customer_Service
   fields = ('email', 'last_name', 'first_name', 'surname', 'comment', 'password')
   success_url = '/accounts/login/'

   def form_valid(self, form):
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      return super().form_valid(form)
   
class CustomerDeleteView(DeleteView):
   model = Customer_Service
   success_url = '/service' 

class CustomerListView(ListView):
   model = Customer_Service

class CustomerDetailView(DetailView):
   model = Customer_Service
   
class CustomerUpdateView(UpdateView):
   model = Customer_Service
   fields = ('email', 'last_name', 'first_name', 'surname', 'comment', 'password')
   success_url = '/service'

   def form_valid(self, form):
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      return super().form_valid(form)

   def get_success_url(self):
      return reverse('service:service', args=[self.kwargs.get('pk')])
   
#---------------------------------------------------------------------------

class SettingsCreateView(LoginRequiredMixin, CreateView):
   model = Settings
   fields = ('mailing_time', 'periodicity', 'mailing_status', 'client')
   success_url = '/service/settings/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Customer_Service.objects.all()
      context['objects'] = settings_objects
      return context

class SettingsDeleteView(DeleteView):
   model = Settings
   success_url = '/service/settings/' 

class SettingsListView(ListView):
   model = Settings

class SettingsDetailView(DetailView):
   model = Settings
   
class SettingsUpdateView(UpdateView):
   model = Settings
   fields = ('mailing_time', 'periodicity', 'mailing_status', 'client')
   success_url = '/service/settings/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Customer_Service.objects.all()
      context['objects'] = settings_objects
      return context
   
#--------------------------------------------------------------

class Message_to_SendCreateView(CreateView):
   model = Message_to_Send
   fields = ('letter_subject', 'letter_body', 'settings')
   success_url = '/service/message/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context

class Message_to_SendDeleteView(DeleteView):
   model = Message_to_Send
   success_url = '/service/message/' 

class Message_to_SendListView(ListView):
   model = Message_to_Send

class Message_to_SendDetailView(DetailView):
   model = Message_to_Send
   
class Message_to_SendUpdateView(UpdateView):
   model = Message_to_Send
   fields = ('letter_subject', 'letter_body', 'settings')
   success_url = '/service/message/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context
   
#--------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class Mailing_LogsCreateView(CreateView):
   model = Mailing_Logs
   fields = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')
   success_url = '/service/logs/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context

class Mailing_LogsDeleteView(DeleteView):
   model = Mailing_Logs
   success_url = '/service/logs/' 

class Mailing_LogsListView(ListView):
   model = Mailing_Logs

class Mailing_LogsDetailView(DetailView):
   model = Mailing_Logs
   
class Mailing_LogsUpdateView(UpdateView):
   model = Mailing_Logs
   fields = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')
   success_url = '/service/logs/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context

#--------------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
 
            response = redirect('/service/')
            response.set_cookie('access_token', access, httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
   logout(request)
      
   response = JsonResponse({"message": "Logout completed successfully"})
   response.delete_cookie('access_token')
   response.delete_cookie('refresh_token')
   return response