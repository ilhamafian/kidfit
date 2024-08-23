from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    first_name = models.CharField(
        max_length=200, null=False, blank=False, default="")
    last_name = models.CharField(
        max_length=200, null=False, blank=False, default="")
    gender = models.CharField(
        max_length=200, null=False, blank=True, default="")
    measurement = models.CharField(
        max_length=200, null=False, blank=True, default="")
    weight = models.CharField(
        max_length=200, null=False, blank=True, default=0)
    height = models.CharField(
        max_length=200, null=False, blank=True, default=0)
    inseam = models.CharField(
        max_length=200, null=False, blank=True, default=0)
    chest = models.CharField(
        max_length=200, null=False, blank=True, default=0)
    waist = models.CharField(
        max_length=200, null=False, blank=True, default=0)
    hip = models.CharField(max_length=200, null=False, blank=True, default=0)
    foot = models.CharField(max_length=200, null=False, blank=True, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SizeCharts(models.Model):
    brand = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    description = models.CharField(max_length=200)
    size_chart = models.JSONField()

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name_plural = "Size Charts"
