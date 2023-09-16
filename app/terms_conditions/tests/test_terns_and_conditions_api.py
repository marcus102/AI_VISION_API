from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Terms, Conditions

TERMS_URL = reverse('terms_conditions:terms-list')
CONDITIONS_URL = reverse('terms_conditions:conditions-list')


class QADataViewTest(TestCase):

  def setUp(self):
    self.client = APIClient()
    res = self.client.get(TERMS_URL)
    res = self.client.get(CONDITIONS_URL)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_get_terms_successful(self):
    '''Test to check if get terms works perfectly.'''
    Terms.objects.create(
      header='the header',
      title='the title',
      body='the body',
    )

    res = self.client.get(TERMS_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    data = res.data[0]
    self.assertEqual(data['header'], 'the header')
    self.assertEqual(data['title'], 'the title')
    self.assertEqual(data['body'], 'the body')
    self.assertTrue(Terms.objects.filter(header='the header').exists())
    self.assertTrue(Terms.objects.filter(title='the title',).exists())
    self.assertTrue(Terms.objects.filter(body='the body').exists())

  def test_get_conditions_successful(self):
    '''Test to check if get conditions works perfectly.'''
    Conditions.objects.create(
      header='the header',
      title='the title',
      body='the body',
    )

    res = self.client.get(CONDITIONS_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    data = res.data[0]
    self.assertEqual(data['header'], 'the header')
    self.assertEqual(data['title'], 'the title')
    self.assertEqual(data['body'], 'the body')
    self.assertTrue(Conditions.objects.filter(header='the header').exists())
    self.assertTrue(Conditions.objects.filter(title='the title',).exists())
    self.assertTrue(Conditions.objects.filter(body='the body').exists())
