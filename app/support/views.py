from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from .serializers import FAQsSerializer, AssistanceSerializer
from core.models import Assistance, FrequentlyAskedQuestions


class FAQsListAPIView(APIView):
  '''Get all FAQ.'''
  serializer_class = FAQsSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    queryset = FrequentlyAskedQuestions.objects.all()
    serializer = FAQsSerializer(queryset, many=True)

    return Response(serializer.data)


class AssistanceAPIView(APIView):
  '''User support manager API.'''

  serializer_class = AssistanceSerializer
  queryset = Assistance.objects.all()
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
    serializer = AssistanceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()
    return Response(serializer.data)
