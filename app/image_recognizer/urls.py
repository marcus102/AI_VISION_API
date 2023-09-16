'''URL mappings for the image api.'''

from django.urls import (
  path,
  include,
)
from rest_framework.routers import DefaultRouter
from image_recognizer import views

router = DefaultRouter()
router.register('image_recognition', views.AI_ImageViewSet)

app_name = 'image_recognizers'

urlpatterns = [
  path('', include(router.urls)),
]
