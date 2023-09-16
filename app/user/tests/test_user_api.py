'''Test for the user api.'''

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
DELETE_URL = reverse('user:delete')
CONFIRM_CODE_URL = reverse('user:confirm_code')
UPDATE_PASSWORD_URL = reverse('user:update_password')


def create_user(**params):
  """Create and return a new user."""
  return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
  """Test the public features of the user API."""

  def setUp(self):
    self.client = APIClient()

  def test_user_with_email_exists_error(self):
    """Test error returned if user with email exists."""
    payload = {
      'email': 'test@example.com',
      'username': '@marcus1',
      'password': 'testpass123',
      'surname': 'Test Surname',
      'last_name': 'My last name',
    }
    create_user(**payload)
    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_user_with_username_exists_error(self):
    """Test error returned if user with username exists."""
    payload = {
      'email': 'test1@example.com',
      'username': '@marcus',
      'password': 'testpass1234',
      'surname': 'Test_Surname',
      'last_name': 'My_last name',
    }
    create_user(**payload)
    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_password_too_short_error(self):
    """Test an error is returned if password less than 5 chars."""
    payload = {
      'email': 'test@example.com',
      'username': '@marcus',
      'password': 'pw',
      'surname': 'Test Surname',
      'last_name': 'My last name',
    }
    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    user_exists = get_user_model().objects.filter(
      email=payload['email'],
      username=payload['username'],
    ).exists()
    self.assertFalse(user_exists)

  def test_create_token_for_user(self):
    """Test generates token for valid credentials."""
    user_details = {
      'surname': 'Test Surname',
      'last_name': 'My last name',
      'email': 'test@example.com',
      'username': '@marcus_t',
      'password': 'test-user-password123',
    }
    create_user(**user_details)
    payload = {
      'username': user_details['username'],
      'email': user_details['email'],
      'password': user_details['password'],
    }
    res = self.client.post(TOKEN_URL, payload)
    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_create_token_bad_credentials(self):
    """Test returns error if credentials invalid."""
    create_user(
      username='@marcusp',
      email='test@example.com',
      password='goodpass'
    )
    payload = {
      'username': '@marcus_t',
      'email': 'test@example.com',
      'password': 'badpass'
    }
    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_email_not_found(self):
    """Test error returned if user not found for given email."""
    payload = {
      'username': '@marcus_t',
      'email': 'test@example.com',
      'password': 'pass123'
    }
    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_username_not_found(self):
    """Test error returned if user not found for given username."""
    payload = {
      'username': '@marcuses',
      'email': 'test@example.com',
      'password': 'pass123'
    }
    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_blank_password(self):
    """Test posting a blank password returns an error."""
    payload = {
      'username': '@marcus',
      'email': 'test@example.com',
      'password': ''
    }
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_retrieve_user_unauthorized(self):
    """Test authentication is required for users."""
    res = self.client.get(ME_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_delete_user_unauthorized(self):
    '''Test authentication is required to delete a user'''

    res = self.client.delete(DELETE_URL)
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

  @patch('user.serializers.Client')
  def test_create_user_and_send_confirmation_code_successful(self, mock_client):
    '''Test confirmation code is successful.'''

    payload = {
      'email': 'test1@example.com',
      'username': '@user1',
      'password': 'testpass123',
      'surname': 'Test Surname',
      'last_name': 'My last name',
      'phone_number': '4345738949',
      'date_of_birth': '2020-04-18',
      'gender': 'male',
      'country': 'BF',
    }

    mock_service = mock_client().verify.services.return_value

    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertTrue(get_user_model().objects.filter(email=payload['email']).exists())
    self.assertTrue(get_user_model().objects.filter(phone_number=payload['phone_number']).exists())
    self.assertTrue(get_user_model().objects.filter(username=payload['username']).exists())
    self.assertNotIn('password', res.data)

    self.assertEqual(mock_client.call_count, 2)
    mock_client.assert_any_call(
      settings.ACCOUNT_SID,
      settings.AUTH_TOKEN
    )

    mock_service.verifications.create.assert_called_once_with(
      to=f'+234{payload["phone_number"]}',
      channel='sms'
    )

  def test_password_update_unsuccessful(self):
    '''Test update user password unsuccessful for unauthenticated user.'''

    payload = {
      'password': 'newpassword123',
    }

    res = self.client.patch(UPDATE_PASSWORD_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertNotIn(payload['password'], res.data)


class PrivateUserApiTests(TestCase):
  """Test API requests that require authentication."""

  def setUp(self):
    self.user = create_user(
      email='test@example.com',
      username='@marcus',
      password='testpass123',
      surname='Test Name',
      last_name='my last name',
      phone_number='+2344345738949',
      date_of_birth='2020-04-18',
      gender='male',
      country='BF',
      confirmation_code='------',
    )
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

  def test_retrieve_profile_success(self):
    """Test retrieving profile for logged in user."""
    res = self.client.get(ME_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertIn(self.user.email, res.data['email'])
    self.assertIn(self.user.username, res.data['username'])
    self.assertIn(self.user.surname, res.data['surname'])
    self.assertIn(self.user.last_name, res.data['last_name'])
    self.assertIn(self.user.phone_number, res.data['phone_number'])
    self.assertIn(self.user.date_of_birth, res.data['date_of_birth'])
    self.assertIn(self.user.gender, res.data['gender'])
    self.assertIn(self.user.country, res.data['country'])
    self.assertIn(self.user.confirmation_code, res.data['confirmation_code'])

  def test_post_me_not_allowed(self):
    """Test POST is not allowed for the me endpoint."""
    res = self.client.post(ME_URL, {})

    self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  def test_update_user_profile(self):
    """Test updating the user profile for the authenticated user."""

    payload = {
      'surname': 'Updated surname',
      'password': 'newpassword123',
    }

    res = self.client.patch(ME_URL, payload)

    self.user.refresh_from_db()
    self.assertEqual(self.user.surname, payload['surname'])
    self.assertTrue(self.user.check_password(payload['password']))
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_delete_user(self):
    '''Test to delete a user'''

    res = self.client.delete(DELETE_URL)
    self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    @patch('user.serializers.Client')
    def test_confirmation_code_correct(self, mock_client):
      '''Test if the confirmation code sent is correct.'''
      mock_service = mock_client().verify.services.return_value
      mock_verification_check = mock_service.verification_checks.create.return_value

      payload = {
        'confirmation_code': '342734'
      }

      mock_verification_check.status = 'approved'
      res = self.client.patch(CONFIRM_CODE_URL, payload)

      self.user.refresh_from_db()
      self.assertEqual(res.status_code, status.HTTP_200_OK)
      self.assertTrue(get_user_model().objects.filter(confirmation_code=payload['confirmation_code']).exists())

      self.assertEqual(mock_client.call_count, 1)
      mock_client.assert_called_once_with(
        settings.ACCOUNT_SID,
        settings.AUTH_TOKEN
      )

      mock_service.verification_checks.create.assert_called_once_with(
        to=f'+234{self.user.phone_number}',
        code=payload['confirmation_code']
      )

      self.assertEqual(mock_verification_check.status, 'approved')
      self.assertTrue(get_user_model().objects.filter(phone_number=self.user.phone_number).exists())
      self.assertEqual(mock_verification_check.to, f'+234{self.user.phone_number}')
      self.assertEqual(mock_verification_check.code, payload['confirmation_code'])
      self.assertEqual(self.user.confirmation_code, payload['confirmation_code'])

  def test_password_update_successful(self):
    '''Test update user password successful.'''
    payload = {
      'password': 'newpassword123',
    }

    res = self.client.patch(UPDATE_PASSWORD_URL, payload)
    self.user.refresh_from_db()
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertTrue(self.user.check_password(payload['password']))
