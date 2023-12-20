'''Serializers for translation APIs.'''

from rest_framework import serializers

class TranslationSerializer(serializers.Serializer):
  original_language = serializers.CharField()
  chosen_language = serializers.CharField()
  original_text = serializers.CharField()
  translated_text = serializers.CharField()

  class Meta:
    fields = ['original_language', 'chosen_language', 'original_text', 'translated_text']
    read_only_fields = ['translated_text']