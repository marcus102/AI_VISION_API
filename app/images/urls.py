'''URL mappings for the image api.'''

from django.urls import (
  path,
  include,
)
from rest_framework.routers import DefaultRouter
from images import views

router = DefaultRouter()
router.register('images', views.ProfileImageViewSet)

app_name = 'image'

urlpatterns = [
  path('', include(router.urls)),
]
