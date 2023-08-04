from django.shortcuts import render
from django.urls import reverse
import requests
from service.models import Customer_Service, Settings, Message_to_Send, Mailing_Logs 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

class CustomerCreateView(CreateView):
   model = Customer_Service
   fields = ('email', 'last_name', 'first_name', 'surname', 'comment')
   success_url = '/accounts/login/'

class CustomerDeleteView(DeleteView):
   model = Customer_Service
   success_url = '/service' 

class CustomerListView(ListView):
   model = Customer_Service

class CustomerDetailView(DetailView):
   model = Customer_Service
   
class CustomerUpdateView(UpdateView):
   model = Customer_Service
   fields = ('email', 'last_name', 'first_name', 'surname', 'comment')
   success_url = '/service'

   def get_success_url(self):
      return reverse('service:service', args=[self.kwargs.get('pk')])
   
#---------------------------------------------------------------------------

class SettingsCreateView(CreateView):
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

#---------------------------------------------------------------

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = self.user
            refresh = self.token
            access = refresh.access_token

            # Сохраняем токены в модели Customer_Service
            try:
                customer = Customer_Service.objects.get(email=user.email)
                customer.access_token = str(access)
                customer.refresh_token = str(refresh)
                customer.save()
            except Customer_Service.DoesNotExist:
                Customer_Service.objects.create(
                    email=user.email,
                    last_name=user.last_name,
                    first_name=user.first_name,
                    access_token=str(access),
                    refresh_token=str(refresh),
                )

            response.data['email'] = user.email
            response.data['name'] = user.first_name  
            response.data['access_token'] = str(access)
            response.data['refresh_token'] = str(refresh)

        return response

class MyTokenRefreshView(TokenRefreshView):
    pass

#--------------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('service:home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')

def logout_view(request):
   logout(request)
   return redirect('login')