from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Assistance, FrequentlyAskedQuestions

SUPPORT_URL = reverse('support:qa-list')
ASSISTANCE_URL = reverse('support:assistance-list')


class QADataViewTest(TestCase):

  def setUp(self):
    self.client = APIClient()

  def test_get_support_successful(self):
    '''Test get suport is successful.'''

    FrequentlyAskedQuestions.objects.create(
      questions='My questions',
      answers='my answers',
    )

    res = self.client.get(SUPPORT_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    data = res.data[0]
    self.assertEqual(data['questions'], 'My questions')
    self.assertEqual(data['answers'], 'my answers')
    self.assertTrue(FrequentlyAskedQuestions.objects.filter(questions='My questions').exists())
    self.assertTrue(FrequentlyAskedQuestions.objects.filter(answers='my answers').exists())

  def test_post_assistance_successful(self):
    '''Test post assistance is successfull.'''

    payload = {
      'email': 'user@example.com',
      'issue_nature': 'my issue nature',
      'issue_detail': 'Details bout issues',
    }

    res = self.client.post(ASSISTANCE_URL, data=payload, format='json')

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data['email'], payload['email'])
    self.assertEqual(res.data['issue_nature'], payload['issue_nature'])
    self.assertEqual(res.data['issue_detail'], payload['issue_detail'])
    self.assertTrue(Assistance.objects.filter(email='user@example.com').exists())
    self.assertTrue(Assistance.objects.filter(issue_nature='my issue nature').exists())
    self.assertTrue(Assistance.objects.filter(issue_detail='Details bout issues').exists())
