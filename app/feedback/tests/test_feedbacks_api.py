from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Feedback

FEEDBACK_URL = reverse('feedback:create-feed')


def detail_url(feedback_id):
  '''Create and return a feedback detail URL.'''
  return reverse('feedback:feedback-detail', args=[feedback_id])


def create_user(**params):
  '''Create and return a new user.'''
  return get_user_model().objects.create_user(**params)


class PublicFeedbackAPITestCase(TestCase):
  '''Test unauthenticated API request'''

  def setUp(self):
    self.client = APIClient()

  def test_auth_required(self):
    '''Test auth is required to call API.'''

    payload = {
      'stars_count': '5 stars',
      'feed': 'feedback section',
    }

    res = self.client.post(FEEDBACK_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITestCase(TestCase):
  '''Test authenticated API request.'''

  def setUp(self):
    self.client = APIClient()
    self.user = create_user(
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

    self.client.force_authenticate(self.user)

  def test_create_feedback(self):
    '''Test creating a feedback.'''

    payload = {
      'stars_count': '4 stars',
      'feed': 'my feed',
    }

    res = self.client.post(FEEDBACK_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    feedback = Feedback.objects.get(id=res.data['id'])
    # k for key and v for value in the payload dictionary
    for k, v in payload.items():
      self.assertEqual(getattr(feedback, k), v)
    self.assertEqual(feedback.user, self.user)
