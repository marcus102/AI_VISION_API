from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

HELP_URL = reverse('support:assistance-list')


class AssistanceTestCase(TestCase):
  '''Test unauthenticated API request'''

  def setUp(self):
    self.client = APIClient()

  def test_create_support(self):
    '''Test create support API.'''

    payload = {
      'email': 'user3@example.com',
      'issue_nature': 'issue',
      'issue_detail': 'my issue here!',
    }

    res = self.client.post(HELP_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data['email'], payload['email'])
    self.assertEqual(res.data['issue_nature'], payload['issue_nature'])
    self.assertEqual(res.data['issue_detail'], payload['issue_detail'])

  def test_create_support_without_email_unsuccessful(self):
    '''Test if user input without an email unseccessful.'''

    payload = {
      'issue_nature': 'issue',
      'issue_detail': 'my issue here!',
      'date': '2023-06-03',
    }

    res = self.client.post(HELP_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertNotIn(payload['issue_nature'], res.data)
    self.assertNotIn(payload['issue_detail'], res.data)
    self.assertNotIn(payload['date'], res.data)
