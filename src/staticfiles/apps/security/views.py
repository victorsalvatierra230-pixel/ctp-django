from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
# Create your views here.

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Has iniciado sesión con éxito {self.request.user}.")
        return response

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.SUCCESS, 'Te esperamos pronto.')
        return response