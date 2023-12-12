'''Serializers for the user API View.'''

from django.contrib.auth import (
  get_user_model,
  authenticate,
)
from core.models import DeletedAccountFeed
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth.hashers import check_password


class UserCodeConfirmationSerializer(serializers.ModelSerializer):
  '''Serializer for user confirmation code.'''

  class Meta:
    model = get_user_model()
    fields = ['confirmation_code']

  def update(self, instance, validated_data):
    '''Updade method.'''

    confirmation_code = validated_data.get('confirmation_code')
    user = super().update(instance, validated_data)

    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN

    client = Client(account_sid, auth_token)

    service_sid = settings.SERVICE_SID
    service = client.verify.services(service_sid)

    verification_code = confirmation_code

    verification_check = service.verification_checks.create(
      to=f'+{user.phone_number}',
      code=verification_code
    )

    if verification_check.status != 'approved':
      raise serializers.ValidationError({'confirmation_code': 'Invalid confirmation code'})
    else:
      user.confirmation_code = verification_code
      user.save()

    return user


class UserCodeConfirmationSendingSerializer(serializers.ModelSerializer):
  '''Send user code for confirmation.'''
  
  class Meta:
    model = get_user_model()
    fields = ['phone_number']

  def update(self, instance, validated_data):
    '''confirmation code for verification.'''
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)
    phone_number = validated_data.pop('phone_number')
    
    service_sid = settings.SERVICE_SID
    service = client.verify.services(service_sid)
    
    service.verifications.create(
      to=f'+{phone_number}',
      channel='sms'
    )

    return super().update(instance, validated_data)
    

class UpdatePasswordSerializer(serializers.ModelSerializer):
  '''Serializer for password update.'''

  class Meta:
    model = get_user_model()
    fields = ['password']
    extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

  def update(self, instance, validated_data):
    '''Manage password update here.'''

    password = validated_data.pop('password', None)
    auth_user = self.context['request'].user
    user = super().update(instance, validated_data)

    if password:
      user.set_password(password)
      user.save()

    return user
  
  # def update(self, instance, validated_data):
  #     '''Manage password update here.'''

  #     password = validated_data.pop('password', None)
  #     old_password = validated_data.pop('old_password', None)
  #     auth_user = self.context['request'].user

  #     if instance.password == old_password:
  #       if instance.password is not None :
  #         instance.password.clear()
  #       instance.set_password(password)
  #       instance.save()
  #     else:
  #         raise serializers.ValidationError('Invalid old password')

  #     return instance


class UserSerializer(serializers.ModelSerializer):
  '''Serializer for the user object.'''

  class Meta:
    model = get_user_model()
    fields = ['id', 'email', 'username', 'password', 'surname', 'last_name', 'phone_number', 'date_of_birth', 'gender', 'country', 'confirmation_code', 'user_status', 'date']
    extra_kwargs = {
      'password': {'write_only': True, 'min_length': 5}
    }
    read_only_fields = ['id', 'date', 'confirmation_code']

  def create(self, validated_data):
    '''Post the confirmation code for verification.'''

    user = get_user_model().objects.create_user(**validated_data)

    return user

  def update(self, instance, validated_data):
    """Update and return user."""

    password = validated_data.pop('password', None)
    user = super().update(instance, validated_data)

    if password:
      user.set_password(password)
      user.save()

    return user

class DeleteAccountFeedSerializer(serializers.ModelSerializer):
  '''Serializer for deleted accounts feedbacks.'''

  class Meta:
    model = DeletedAccountFeed
    fields = ['id', 'anonymous', 'reason', 'date']
    only_read_fields = ['id', 'date']
    extra_kwargs = {
      'anonymous': {'default': 'Anonymous'},
      'reason': {'default': 'None'}
    }

  def create(self, validated_data):
    return super().create(validated_data)


class AuthTokenSerializer(serializers.Serializer):
  """Serializer for the user auth token."""

  email = serializers.EmailField()
  password = serializers.CharField(
    style={'input_type': 'password'},
    trim_whitespace=False,
  )

  def validate(self, attrs):
    """Validate and authenticate the user."""

    email = attrs.get('email')
    password = attrs.get('password')

    user = authenticate(
      request=self.context.get('request'),
      email=email,
      password=password,
    )


    if not user:
      msg = _('Unable to authenticate with provided credentials.')
      raise serializers.ValidationError(msg, code='authorization')

    attrs['user'] = user
    return attrs
