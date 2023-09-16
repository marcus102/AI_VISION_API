from core.models import FrequentlyAskedQuestions, Assistance
from rest_framework import serializers


class FAQsSerializer(serializers.ModelSerializer):
  '''Serializer for FAQs'''

  class Meta:
    model = FrequentlyAskedQuestions
    fields = ['id', 'questions', 'answers']
    only_read_fields = ['id']


class AssistanceSerializer(serializers.ModelSerializer):
  '''Serializer for FAQs'''

  class Meta:
    model = Assistance
    fields = ['id', 'email', 'issue_nature', 'issue_detail', 'date']
    only_read_fields = ['id', 'date']
