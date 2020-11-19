from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .forms import UserRegisterForm, UserUpdateForm

from django.contrib.auth.models import User
# Create your views here.

class RegisterView(generic.FormView):
    form_class = UserRegisterForm
    
    template_name = 'users/register.html'

    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        print(form)
        form.save()
        messages.success(self.request, 'Account registered! You can now log in.')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.info(self.request, 'Could not register. Please check that the fields are filled out correctly.')
        return redirect(reverse_lazy('users:register'))



class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    
    redirect_field_name = reverse_lazy('polls:index')
    
    def form_invalid(self, form, *args, **kwargs):
        messages.info(self.request, 'Login failed due to incorrect data.')
        return redirect(reverse_lazy('users:login'))

    def form_valid(self, form):
        messages.success(self.request, 'Logged in. Welcome, %s!' % self.request.POST['username'])
        super().form_valid(form)
        return redirect(self.redirect_field_name)


class ProfileView(generic.UpdateView):
    form_class = UserUpdateForm

    template_name = 'users/profile.html'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Changes saved.')
        return redirect(reverse_lazy('users:user_profile', kwargs={'pk':self.request.user.pk}))
    
    def form_invalid(self, form):
        messages.info(self.request, 'Could not save changes. Please check that the fields are filled out correctly.')
        return redirect(reverse_lazy('users:user_profile', kwargs={'pk':self.request.user.pk}))