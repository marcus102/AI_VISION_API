'''Django admin customization.'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
  '''Define the admin pages for users'''
  ordering = ['id']
  list_display = ['email', 'username', 'surname', 'last_name']
  fieldsets = (
    (
      _('Edit Your Infos'),
      {
        'fields': (
          'email',
          'username',
          'surname',
          'last_name',
          'phone_number',
          'date_of_birth',
          'gender',
          'country',
          'user_status',
        )
      }
    ),
    (
      _('User Permissions'),
      {
        'fields': (
          'is_active',
          'is_staff',
          'is_superuser',
        )
      }
    ),
    (_('Important dates'), {'fields': ('last_login',)}),
  )
  readonly_fields = ['last_login']
  add_fieldsets = (
    (
      _('Add a new user'),
      {
        'classes': ('wide',),
        'fields': (
          'email',
          'password1',
          'password2',
          'username',
          'surname',
          'last_name',
          'phone_number',
          'date_of_birth',
          'gender',
          'country',
          'is_active',
          'is_staff',
          'is_superuser',
        )
      }
    ),
  )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.DeletedAccountFeed)
admin.site.register(models.Feedback)
admin.site.register(models.FrequentlyAskedQuestions)
admin.site.register(models.Assistance)
admin.site.register(models.Terms)
admin.site.register(models.Conditions)
admin.site.register(models.ProfileImage)
admin.site.register(models.Predictions)
