'''Views for the feedback APIs'''
from rest_framework import generics
from core.models import Feedback
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import FeedbackSerializer


class FeedbackViewSet(generics.CreateAPIView):
  '''View for manage feedback APIs.'''

  serializer_class = FeedbackSerializer
  queryset = Feedback.objects.all()
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    '''Retrieve feedbacks for autenticated user.'''

    return self.queryset.filter(
      user=self.request.user
    ).order_by('-id').distinct()

  def perform_create(self, serializer):
    '''Create a new feedback.'''
    serializer.save(user=self.request.user)
