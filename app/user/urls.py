'''Url mappings forn the user API.'''

from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
  path('create/', views.CreateUserView.as_view(), name='create'),
  path('token/', views.CreateTokenView.as_view(), name='token'),
  path('me/', views.ManageUserView.as_view(), name='me'),
  path('delete/', views.DeleteUserView.as_view(), name='delete'),
  path('confirm_code/', views.ConfirmationCodeView.as_view(), name='confirm_code'),
  path('send_confirmation_code/', views.UserCodeConfirmationSendingView.as_view(), name='send_confirmation_code'),
  path('update_password/', views.UpdatePasswordView.as_view(), name='update_password'),
  path('delete_account_feed/', views.DeleteAccountFeedView.as_view(), name='delete_account_feed'),
]
