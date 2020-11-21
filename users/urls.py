from django.urls import path

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
]
