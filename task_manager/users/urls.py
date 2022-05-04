from django.urls import path

from task_manager.users.views import (
    UserCreationView, UserDeletingView, UserListView, UserUpdatingView
)


urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('create/', UserCreationView.as_view(), name='create_user'),
    path('<int:pk>/update/', UserUpdatingView.as_view(), name='update_user'),
    path('<int:pk>/delete/', UserDeletingView.as_view(), name="delete_user"),
]
