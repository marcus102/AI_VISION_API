from rest_framework import serializers
from core.models import AI_Image


class AI_ImageSerializer(serializers.ModelSerializer):
  '''Serializer for AI_Image api.'''

  class Meta:
      model = AI_Image
      fields = ['id', 'image', 'image_name', 'image_details', 'link', 'likes', 'favorites', 'shares', 'user_experience', 'date']
      read_only_fields = ['id', 'image_name', 'image_details', 'link', 'date']
      extra_kwargs = {'image': {'required': True}}
