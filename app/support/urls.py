from django.urls import path
from .views import FAQsListAPIView, AssistanceAPIView

app_name = 'support'

urlpatterns = [
  path('qa/', FAQsListAPIView.as_view(), name='qa-list'),
  path('assistance/', AssistanceAPIView.as_view(), name='assistance-list'),
]
