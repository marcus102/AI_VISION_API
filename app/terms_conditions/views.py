from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from .serializers import TermsSerializer, ConditionsSerializer
from core.models import Terms, Conditions


class ConditionsAPIView(APIView):
  '''Get Terms.'''
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    queryset = Conditions.objects.all()
    serializer = ConditionsSerializer(queryset, many=True)
    return Response(serializer.data)


class TermsAPIView(APIView):
  '''Get Conditions.'''
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    queryset = Terms.objects.all()
    serializer = TermsSerializer(queryset, many=True)
    return Response(serializer.data)
