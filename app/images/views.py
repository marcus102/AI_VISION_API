from rest_framework import viewsets
from core.models import ProfileImage
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileImageSerializer
from rest_framework.decorators import action


class ProfileImageViewSet(viewsets.ModelViewSet):
  '''View for manage Image APIs.'''
  serializer_class = ProfileImageSerializer
  queryset = ProfileImage.objects.all()
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    '''Retrieve images for autenticated user.'''

    queryset = self.queryset
    return queryset.filter(
      user=self.request.user
    ).order_by('-id').distinct()

  def perform_create(self, serializer):
    '''Create a new image.'''
    serializer.save(user=self.request.user)
  

