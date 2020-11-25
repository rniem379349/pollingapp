from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.models import User
from polls.models import Question
from .models import Profile
# Create your views here.

class RegisterView(generic.FormView):
    form_class = UserRegisterForm
    
    template_name = 'users/register.html'

    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        username = User.objects.filter(username=self.request.POST['username']).first()
        profile = Profile(user=username)
        profile.save()
        messages.success(self.request, 'Account registered! You can now log in.')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.info(self.request, 'Could not register. Please check that the fields are filled out correctly.')
        return render(self.request, self.template_name, {'form': form})


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    
    redirect_field_name = reverse_lazy('polls:index')
    
    def form_invalid(self, form, *args, **kwargs):
        messages.info(self.request, 'Login failed. Please try again.')
        return redirect(reverse_lazy('users:login'))

    def form_valid(self, form):
        messages.success(self.request, 'Logged in. Welcome, %s!' % self.request.POST['username'])
        super().form_valid(form)
        return redirect(self.redirect_field_name)


class ProfileEditView(generic.UpdateView, LoginRequiredMixin):
    form_class = UserUpdateForm
    second_form_class = ProfileUpdateForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)   

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(instance=self.get_object())
        profile_form = ProfileUpdateForm(instance=self.get_object())

        return self.render_to_response(
            self.get_context_data(
                user_form=form,
                profile_form=profile_form,
            )
        )
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            profile_form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Changes saved.')
        return redirect(reverse_lazy('users:user_profile', kwargs={'pk':self.request.user.pk}))
    
    def form_invalid(self, form):
        messages.info(self.request, 'Could not save changes. Please check that the fields are filled out correctly.')
        return redirect(reverse_lazy('users:user_profile', kwargs={'pk':self.request.user.pk}))


# class ProfileEditView(generic.UpdateView, LoginRequiredMixin):
#     form_class = UserUpdateForm
#     second_form_class = ProfileUpdateForm
#     template_name = 'users/profile.html'

#     def get_queryset(self):
#         return User.objects.filter(pk=self.request.user.pk)   

#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
    
#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, 'Changes saved.')
#         return redirect(reverse_lazy('users:user_profile', kwargs={'pk':self.request.user.pk}))
    
#     def form_invalid(self, form):
#         messages.info(self.request, 'Could not save changes. Please check that the fields are filled out correctly.')
#         return redirect(reverse_lazy('users:user_profile', kwargs={'pk':self.request.user.pk}))


class ProfileView(generic.ListView):
    model = Question
    template_name = 'users/profile_page.html'
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, username=self.kwargs.get('username'))
        context["profile"] = Profile.objects.get(user=context['user'])
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
        qs = Question.objects.filter(user=user)
        indexes = self.get_question_indexes_odd_or_not(qs)
        res = zip(qs, indexes)
        return res