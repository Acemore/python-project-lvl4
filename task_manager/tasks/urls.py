from django.urls import path

from .views import (
    TaskCreationView, TaskDeletingView, TaskDetailsView,
    TasksListView, TaskUpdatingView
)


urlpatterns = [
    path('', TasksListView.as_view(), name='tasks'),
    path('create/', TaskCreationView.as_view(), name='create_task'),
    path('<int:pk>/update/', TaskUpdatingView.as_view(), name='update_task'),
    path('<int:pk>/delete/', TaskDeletingView.as_view(), name='delete_task'),
    path('<int:pk>/', TaskDetailsView.as_view(), name='details'),
]
