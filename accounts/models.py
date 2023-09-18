from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.email


class ChildInfo(models.Model):
    childs_name = models.CharField(max_length=200, null=False, blank=False),
    gender = models.CharField(max_length=200, null=False, blank=False),
    measurements = models.CharField(max_length=200, null=False, blank=False),
    weight = models.CharField(max_length=200, null=False, blank=False),
    height = models.CharField(max_length=200, null=False, blank=False),
    inseam = models.CharField(max_length=200, null=False, blank=False),
    chest = models.CharField(max_length=200, null=False, blank=False),
    waist = models.CharField(max_length=200, null=False, blank=False),
    hip = models.CharField(max_length=200, null=False, blank=False),
    foot = models.CharField(max_length=200, null=False, blank=False),

    def __str__(self):
        return self.childs_name
