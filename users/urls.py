from django.urls import include, path, reverse_lazy

from django.contrib.auth import views as auth_views

from . import views

# specify app name for namespacing later when referencing the url path names
app_name = 'users'

urlpatterns = [
    path('<str:username>/profile', views.ProfileView.as_view(), name='profile_page'),
    path('<int:pk>/edit', views.ProfileEditView.as_view(), name='user_profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), 
        name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
]