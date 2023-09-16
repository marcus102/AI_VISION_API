from rest_framework import serializers
from core.models import ProfileImage


class ProfileImageSerializer(serializers.ModelSerializer):
  '''Serializer for Image.'''

  class Meta:
    model = ProfileImage
    fields = ['id', 'image', 'date']
    read_only_fields = ['id', 'date']
    extra_kwargs = {'image': {'required': 'True'}}
