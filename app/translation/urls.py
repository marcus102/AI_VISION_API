'''URL mappings for the translation app.'''

from django.urls import path
from .views import TranslationViewSet

app_name = 'translation'

urlpatterns = [
  path('translate/', TranslationViewSet.as_view(), name='translate'),
]
