from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "tasks"

urlpatterns = [
    path('', views.TaskPageView().as_view, name = 'tasks_page'),
    path('about/', views.tasks_page_about, name = 'tasks_page_about'),
    path('details/<int:pk>', views.task_details, name = 'task_details'),
    path('create/', views.CreateTaskView().as_view, name = 'create_task'),
]
