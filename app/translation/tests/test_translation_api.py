from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from core.models import Translation

TRANSLATION_URL = reverse('translation:translate')


class TranslationAPITestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

  @patch('translation.views.Translator')
  def test_create_translation(self, mock_translate):
    '''Test translate is successful.'''

    mock_translate.return_value.translate.return_value.text = 'Bonjour'

    payload = {
      'translated_text_id': 'id1',
      'original_text_id': 's',
      'original_language': 'english',
      'chosen_language': 'french',
      'original_text': 'Hello',
    }
    response = self.client.post(TRANSLATION_URL, data=payload, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    translation = Translation.objects.get(pk=response.data['id'])
    self.assertEqual(translation.original_language, 'english')
    self.assertEqual(translation.chosen_language, 'french')
    self.assertEqual(translation.original_text, 'Hello')
    self.assertEqual(translation.translated_text, 'Bonjour')
