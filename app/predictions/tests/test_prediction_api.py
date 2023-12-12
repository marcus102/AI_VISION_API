import tempfile
from unittest import TestCase
from PIL import Image
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from core.models import Predictions

PREDICTION_URL = reverse('prediction:prediction-list')


def create_user(**params):
  return get_user_model().objects.create_user(**params)


def image_upload_url(image_id):
  '''Create and return an image upload URL.'''
  return reverse('image:profileimage-detail', args=[image_id])


class PulbicTestCase(TestCase):

  def setUp(self):
    self.client = APIClient()

  def test_image_upload_unsuccessful(self):
    '''Test that image is not uploaded successfully for an unauthenticated user.'''
    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
      img = Image.new('RGB', (10, 10))
      img.save(image_file, format='JPEG')
      image_file.seek(0)
      payload = {'image': image_file}
      res = self.client.post(PREDICTION_URL, payload, format='multipart')

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
