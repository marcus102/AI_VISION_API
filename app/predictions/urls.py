'''URL mappings for the image api.'''

from django.urls import (
  path,
  include,
)
from rest_framework.routers import DefaultRouter
from .views import PredictionViewSet

router = DefaultRouter()
router.register('predictions', PredictionViewSet)

app_name = 'prediction'

urlpatterns = [
  path('', include(router.urls)),
]
