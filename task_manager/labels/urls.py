from django.urls import path

from .views import (
    LabelCreationView, LabelDeletingView, LabelsListView, LabelUpdatingView
)


urlpatterns = [
    path('', LabelsListView.as_view(), name='labels'),
    path('create/', LabelCreationView.as_view(), name='create_label'),
    path('<int:pk>/update/', LabelUpdatingView.as_view(), name='update_label'),
    path('<int:pk>/delete/', LabelDeletingView.as_view(), name='delete_label'),
]
