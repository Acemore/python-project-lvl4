from django.urls import path

from .views import (
    StatusCreationView, StatusDeletingView,
    StatusesListView, StatusUpdatingView,
)


urlpatterns = [
    path('', StatusesListView.as_view(), name='statuses'),
    path('create/', StatusCreationView.as_view(), name='create_status'),
    path(
        '<int:pk>/update/', StatusUpdatingView.as_view(), name='update_status'
    ),
    path(
        '<int:pk>/delete/', StatusDeletingView.as_view(), name='delete_status'
    ),
]
