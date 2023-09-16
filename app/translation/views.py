'''Views for the translation APIs'''
from rest_framework import (
  generics,
  authentication,
  permissions,
)
from core.models import Translation
from rest_framework.response import Response
from .serializers import TranslationSerializer
from googletrans import Translator


class TranslationViewSet(generics.ListAPIView):
  '''Create a translation API.'''

  serializer_class = TranslationSerializer
  queryset = Translation.objects.all()
  authentication_classes = [authentication.TokenAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, *args, **kwargs):
    text_id = request.data.get('text_id')
    original_language = request.data.get('original_language', 'english')
    chosen_language = request.data.get('chosen_language', 'english')
    original_text = request.data.get('original_text', 'english')

    language_codes = {
      'english': 'en',
      'french': 'fr',
      'spanish': 'es',
      'chinese': 'zh',
      'portuguese': 'pt',
    }
    language_code = language_codes.get(chosen_language.lower())

    if not language_code:
      return Response({'error': 'Invalid target language.'}, status=400)

    translator = Translator()
    translated = translator.translate(original_text, src=original_language, dest=language_code)
    translated_text = translated.text

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(
      text_id=text_id,
      original_language=original_language,
      chosen_language=chosen_language,
      original_text=original_text,
      translated_text=translated_text,
    )
    return Response(serializer.data, status=201)
