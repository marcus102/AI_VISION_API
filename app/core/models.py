'''Database models.'''

import uuid
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def profile_image_file_path(instance, filename):
    '''Generate file  path for new profile image.'''
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'image', filename)


class UserManager(BaseUserManager):
    '''Manager for users.'''

    def create_user(self, email, password=None, **extra_fields):
        '''Create save and return a new user.'''
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        '''Create and return a new superuser.'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''User in the system.'''

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    surname = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    confirmation_code = models.CharField(max_length=10, default='******')
    user_status = models.CharField(default='Active', max_length=10)
    date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class DeletedAccountFeed(models.Model):
    '''Feeds for deleted accounts'''

    anonymous = models.CharField(max_length=50)
    reason = models.TextField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.anonymous} deleted his account click to check the reasons - {self.date}"


class Feedback(models.Model):
    '''User Feedbacks.'''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    stars_count = models.CharField(max_length=20)
    feed = models.TextField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.stars_count} from {self.user}"


class FrequentlyAskedQuestions(models.Model):
    '''Manage FAQ'''
    questions = models.TextField()
    answers = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.questions} - {self.date}'


class Assistance(models.Model):
    '''Manage Assistance'''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    email = models.EmailField(max_length=255)
    issue_nature = models.CharField(max_length=1000)
    issue_detail = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"From {self.email}: {self.issue_nature} - {self.date}"


class Terms(models.Model):
    '''Manage Terms.'''

    option = models.CharField(max_length=250)
    header = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} updated - {self.date}"


class Conditions(models.Model):
    '''Manage conditions.'''

    option = models.CharField(max_length=250)
    header = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    body = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} updated - {self.date}"


class ProfileImage(models.Model):
    '''Manage profile image.'''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to=profile_image_file_path)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Image uploaded by {self.user} - {self.date}"


class Predictions(models.Model):
    '''Manage AI image recognition.'''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to=profile_image_file_path)
    prediction = models.TextField(default='None')
    image_details = models.TextField(default='None')
    link = models.TextField(default='None')
    likes = models.CharField(default='No', max_length=50)
    favorites = models.CharField(default='No', max_length=50)
    shares = models.CharField(default='No', max_length=50)
    user_experience = models.CharField(default='None', max_length=50)
    status = models.CharField(default='Active', max_length=10)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.prediction} - by {self.user} at {self.date}"
