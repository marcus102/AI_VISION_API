'''Serializers for translation APIs.'''

from rest_framework import serializers
from core.models import Translation


class TranslationSerializer(serializers.ModelSerializer):
  '''Serializer for translation'''

  class Meta:
    model = Translation
    fields = ['id', 'text_id', 'original_language', 'chosen_language', 'original_text', 'translated_text']
    read_only_fields = ['id', 'translated_text']
