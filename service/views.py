from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from service.models import Customer_Service, Settings, Message_to_Send, Mailing_Logs 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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

#@method_decorator(login_required, name='dispatch')
class CustomerDeleteView(DeleteView):
   model = Customer_Service
   success_url = '/service' 


class CustomerListView(ListView):
   model = Customer_Service

@method_decorator(login_required, name='dispatch')
class CustomerDetailView(DetailView):
   model = Customer_Service

@method_decorator(login_required, name='dispatch')
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
@method_decorator(login_required, name='dispatch')
class SettingsCreateView(CreateView):
   model = Settings
   fields = ('mailing_time', 'periodicity', 'mailing_status', 'client')
   success_url = '/service/settings/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Customer_Service.objects.all()
      context['objects'] = settings_objects
      return context

@method_decorator(login_required, name='dispatch')
class SettingsDeleteView(DeleteView):
   model = Settings
   success_url = '/service/settings/' 
   
@method_decorator(login_required, name='dispatch')
class SettingsListView(ListView):
   model = Settings

@method_decorator(login_required, name='dispatch')
class SettingsDetailView(DetailView):
   model = Settings

@method_decorator(login_required, name='dispatch')
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
@method_decorator(login_required, name='dispatch')
class Message_to_SendCreateView(CreateView):
   model = Message_to_Send
   fields = ('letter_subject', 'letter_body', 'settings')
   success_url = '/service/message/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context
   
@method_decorator(login_required, name='dispatch')
class Message_to_SendDeleteView(DeleteView):
   model = Message_to_Send
   success_url = '/service/message/' 

@method_decorator(login_required, name='dispatch')
class Message_to_SendListView(ListView):
   model = Message_to_Send
   
@method_decorator(login_required, name='dispatch')
class Message_to_SendDetailView(DetailView):
   model = Message_to_Send

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class Mailing_LogsDeleteView(DeleteView):
   model = Mailing_Logs
   success_url = '/service/logs/' 

@method_decorator(login_required, name='dispatch')
class Mailing_LogsListView(ListView):
   model = Mailing_Logs

@method_decorator(login_required, name='dispatch')
class Mailing_LogsDetailView(DetailView):
   model = Mailing_Logs

@method_decorator(login_required, name='dispatch')
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
            return redirect('/service/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')

def logout_view(request):
   logout(request)
   response = JsonResponse({"message": "Logout completed successfully"})
   return redirect('http://127.0.0.1:8000/accounts/login/')