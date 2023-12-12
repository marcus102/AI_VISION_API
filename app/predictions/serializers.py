'''Serializers for Feedback APIs.'''

from rest_framework import serializers
from core.models import Predictions


class PredictionSerializer(serializers.ModelSerializer):
  '''Serializer for feedbacks.'''

  class Meta:
    model = Predictions
    fields = ['id', 'image', 'prediction', 'image_details', 'link',
              'likes', 'favorites', 'shares', 'user_experience', 'status', 'date']
    read_only_fields = ['id', 'date']
