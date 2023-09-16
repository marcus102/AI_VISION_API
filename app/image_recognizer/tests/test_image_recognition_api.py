import tempfile
from unittest import TestCase
from PIL import Image
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from core.models import AI_Image

AI_IMAGE_URL = reverse('image_recognizers:ai_image-list')


def my_image(image_id):
  '''Create and return image upload URL.'''
  return reverse('image_recognizers:ai_image-detail', args=[image_id])


def create_user(**params):
  return get_user_model().objects.create_user(**params)


def create_image():
  with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
    img = Image.new('RGB', (10, 10))
    img.save(image_file, format='JPEG')
    image_file.seek(0)
  return image_file


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
      res = self.client.post(AI_IMAGE_URL, payload, format='multipart')

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestCase(TestCase):
  '''Test for authenticated users.'''

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.user = create_user(
      email='user@example.com',
      username='@user',
      password='testpass123',
      surname='Surname',
      last_name='Last Name',
      phone_number='554495349',
      date_of_birth='2020-04-23',
      gender='male',
      country='BF',
    )

  def setUp(self):
    self.client = APIClient()
    self.client.force_authenticate(self.user)

  def test_create_image_success(self):
    '''Test that image is uploaded successfully for an authenticated user.'''

    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
      img = Image.new('RGB', (10, 10))
      img.save(image_file, format='JPEG')
      image_file.seek(0)
      payload = {'image': image_file}
      res = self.client.post(AI_IMAGE_URL, payload, format='multipart')

    self.user.refresh_from_db()
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertIn('image', res.data)
    self.assertNotIn(self.user, res.data)

  def test_delete_image_success(self):
    '''Test that an authenticated user can delete their uploaded image.'''

    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
      img = Image.new('RGB', (10, 10))
      img.save(image_file, format='JPEG')
      image_file.seek(0)
      payload = {'image': image_file}
      create_res = self.client.post(AI_IMAGE_URL, payload, format='multipart')

    image_id = create_res.data.get('id')

    delete_res = self.client.delete(my_image(image_id))

    self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
    self.assertFalse(AI_Image.objects.filter(id=image_id).exists())

  def test_update_image_success(self):
    '''Test that an authenticated user can update their uploaded image.'''

    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
      img = Image.new('RGB', (10, 10))
      img.save(image_file, format='JPEG')
      image_file.seek(0)
      payload = {'image': image_file}
      create_res = self.client.post(AI_IMAGE_URL, payload, format='multipart')

    image_id = create_res.data.get('id')

    with tempfile.NamedTemporaryFile(suffix='.jpg') as new_image_file:
      new_img = Image.new('RGB', (20, 20))
      new_img.save(new_image_file, format='JPEG')
      new_image_file.seek(0)
      update_payload = {'image': new_image_file}
      update_res = self.client.patch(my_image(image_id), update_payload, format='multipart')

    self.assertEqual(update_res.status_code, status.HTTP_200_OK)
    self.assertNotEqual(create_res.data['image'], update_res.data['image'])

  def test_total_update_image_success(self):
    '''Test to totaly update  image successfully.'''

    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
      img = Image.new('RGB', (10, 10))
      img.save(image_file, format='JPEG')
      image_file.seek(0)
      payload = {'image': image_file}
      create_res = self.client.post(AI_IMAGE_URL, payload, format='multipart')

    image_id = create_res.data.get('id')

    with tempfile.NamedTemporaryFile(suffix='.jpg') as new_image_file:
      new_img = Image.new('RGB', (20, 20))
      new_img.save(new_image_file, format='JPEG')
      new_image_file.seek(0)
      update_payload = {
        'image': new_image_file,
        'likes': 'yes',
        'favorites': 'yes',
        'shares': 'yes',
        'user_experience': 'good',
        'date': AI_Image.date,
      }
      update_res = self.client.put(my_image(image_id), update_payload, format='multipart')
    self.user.refresh_from_db()
    self.assertEqual(update_res.status_code, status.HTTP_200_OK)
    self.assertNotEqual(create_res.data['image'], update_res.data['image'])
