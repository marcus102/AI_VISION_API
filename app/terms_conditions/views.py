from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from .serializers import TermsSerializer, ConditionsSerializer
from core.models import Terms, Conditions


class ConditionsAPIView(APIView):
  '''Get Terms.'''
  serializer_class = ConditionsSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    queryset = Conditions.objects.all()
    serializer = ConditionsSerializer(queryset, many=True)
    return Response(serializer.data)


class TermsAPIView(APIView):
  '''Get Conditions.'''
  serializer_class = TermsSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    queryset = Terms.objects.all()
    serializer = TermsSerializer(queryset, many=True)
    return Response(serializer.data)
