'''Views for the user API.'''

from rest_framework import (
  generics, 
  authentication, 
  permissions,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
  UserSerializer,
  AuthTokenSerializer,
  UserCodeConfirmationSerializer,
  UpdatePasswordSerializer,
  UserCodeConfirmationSendingSerializer,
  DeleteAccountFeedSerializer,
)
from django.contrib.auth import get_user_model


class CreateUserView(generics.CreateAPIView):
  '''Create a new user in the system.'''
  serializer_class = UserSerializer


class ConfirmationCodeView(generics.UpdateAPIView):
  '''user conformation code.'''
  serializer_class = UserCodeConfirmationSerializer
  queryset = get_user_model().objects.values('confirmation_code')
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    """Retrieve and return the authenticated user."""
    return self.request.user


class UserCodeConfirmationSendingView(generics.UpdateAPIView):
  '''User code confirmation sending view.'''

  serializer_class = UserCodeConfirmationSendingSerializer
  queryset = get_user_model().objects.values('phone_number')
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    """Retrieve and return the authenticated user."""
    return self.request.user


class UpdatePasswordView(generics.UpdateAPIView):
  '''Update your password here.'''
  serializer_class = UpdatePasswordSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    """Retrieve and return the authenticated user."""
    return self.request.user


class CreateTokenView(ObtainAuthToken):
  '''Create a new auth token for user.'''
  serializer_class = AuthTokenSerializer
  renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
  """Manage the authenticated user."""
  serializer_class = UserSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    """Retrieve and return the authenticated user."""
    return self.request.user


class DeleteUserView(generics.DestroyAPIView):
  '''Delete the user'''
  serializer_class = UserSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self):
    """Retrieve and return the authenticated user."""
    return self.request.user

class DeleteAccountFeedView( generics.CreateAPIView):
  '''Feedback for account deletion.'''
  serializer_class = DeleteAccountFeedSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]
