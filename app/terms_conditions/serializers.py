from core.models import Terms, Conditions
from rest_framework import serializers


class TermsSerializer(serializers.ModelSerializer):
  '''Serializer for Terms'''

  class Meta:
    model = Terms
    fields = ['id', 'option', 'header', 'title', 'body', 'date']
    only_read_fields = ['id', 'date']


class ConditionsSerializer(serializers.ModelSerializer):
  '''Serializer for Conditions'''

  class Meta:
    model = Conditions
    fields = ['id', 'option', 'header', 'title', 'body', 'date']
    only_read_fields = ['id', 'date']
