from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm

from django.contrib.auth.models import User
from polls.models import Question
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


class ProfileEditView(generic.UpdateView, LoginRequiredMixin):
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


class ProfileView(generic.ListView):
    model = Question
    template_name = 'users/profile_page.html'
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(User, username=self.kwargs.get('username'))
        print(context)
        return context
    
    def get_question_indexes_odd_or_not(self, object_list):
        """
        Check if the question's index is odd, for styling odd and even questions with different colors
        """
        indexes = []
        for index, item in enumerate(object_list):
            indexes.append(index % 2 == 0)
        return indexes

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        print(self.kwargs.get('username'))
        print(user)
        qs = Question.objects.filter(user=user)
        indexes = self.get_question_indexes_odd_or_not(qs)
        res = zip(qs, indexes)
        return res