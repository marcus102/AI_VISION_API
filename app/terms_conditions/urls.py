from django.urls import path
from .views import TermsAPIView, ConditionsAPIView

app_name = 'terms_conditions'

urlpatterns = [
  path('terms/', TermsAPIView.as_view(), name='terms-list'),
  path('conditions/', ConditionsAPIView.as_view(), name='conditions-list'),
]
