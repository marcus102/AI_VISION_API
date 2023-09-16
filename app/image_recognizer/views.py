from rest_framework import viewsets
from core.models import AI_Image
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AI_ImageSerializer


class AI_ImageViewSet(viewsets.ModelViewSet):
  '''Manage AI image view api.'''

  serializer_class = AI_ImageSerializer
  queryset = AI_Image.objects.all()
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
