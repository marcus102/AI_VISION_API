'''Views for the translation APIs'''
from rest_framework import (
    generics,
    authentication,
    permissions,
)
from rest_framework.response import Response
from .serializers import TranslationSerializer
from googletrans import Translator, LANGUAGES


class TranslationViewSet(generics.ListAPIView):
  '''Create a translation API.'''

  serializer_class = TranslationSerializer
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]


  def post(self, request, *args, **kwargs):

    original_language = request.data.get('original_language', 'en')
    if original_language not in LANGUAGES:
      return Response({'error': f'Invalid source language: {original_language}.'}, status=400)

    chosen_language = request.data.get('chosen_language', 'en')
    if chosen_language not in LANGUAGES:
      return Response({'error': f'Invalid target language: {chosen_language}.'}, status=400)

    original_text = request.data.get('original_text', '')
    if not original_text:
      return Response({'error': 'Missing original text.'}, status=400)

    translator = Translator()
    try:
      translated = translator.translate(
        original_text, src=original_language, dest=chosen_language)
    except ValueError as e:
      return Response({'error': f'Translation failed: {e}.'}, status=500)

    translated_text = translated.text

    translation_data = {
      'original_language': original_language,
      'chosen_language': chosen_language,
      'original_text': original_text,
      'translated_text': translated_text,
    }

    serializer =  TranslationSerializer(data=translation_data)
    serializer.is_valid(raise_exception=True)
    response_data = serializer.validated_data
    
    return Response(response_data, status=201)
