from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('task/', views.ListTodoView.as_view(), name="task-all"),
    path('task/<int:id>/', views.TodoDetailView.as_view(), name="task-detail"),
]