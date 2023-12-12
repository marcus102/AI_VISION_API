'''URL mappings for the feedback api.'''

from django.urls import path
from .views import FeedbackViewSet

app_name = 'feedback'

urlpatterns = [
  path('create_feed/', FeedbackViewSet.as_view(), name='create-feed'),
]
