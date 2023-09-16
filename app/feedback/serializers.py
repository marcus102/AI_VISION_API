'''Serializers for Feedback APIs.'''

from rest_framework import serializers
from core.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
  '''Serializer for feedbacks.'''

  class Meta:
    model = Feedback
    fields = ['id', 'stars_count', 'feed', 'date']
    read_only_fields = ['id', 'date']
