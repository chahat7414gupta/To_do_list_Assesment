# taskmanager/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='task_list'),  
    path('add/', views.add_task, name='add_task'),
    path('api/tasks/', views.api_tasks, name='api_tasks'),
    path('api/tasks/<int:task_id>/', views.api_task_detail, name='api_task_detail'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'), 
    path('completed/', views.completed_tasks, name='completed_tasks'),
]
