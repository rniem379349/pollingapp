from django.urls import path

from . import views

# specify app name for namespacing later when referencing the url path names
app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.QuestionCreateView.as_view(), name='create-question'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.QuestionEditView.as_view(), name='edit-question'),
    path('<int:pk>/delete', views.QuestionDeleteView.as_view(), name='delete-question'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/comment/', views.CommentCreateView.as_view(), name='create-comment'),
]