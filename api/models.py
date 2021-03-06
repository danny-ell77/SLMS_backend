from turtle import ondrag
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
import datetime
from .managers import CustomUserManager


class TimestampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_date', '-modified_date']


class UserClass(TimestampedModel):
    name = models.CharField(verbose_name='class_name',
                            max_length=20, unique=True, blank=False)

    class Meta:
        verbose_name_plural = "User Classes"

    def __str__(self) -> str:
        return self.name


# To be used explicitly for Authentication, Authorization & Permisions
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
        ('INSTRUCTOR', 'Instructor')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    _class = models.ForeignKey(UserClass, on_delete=models.CASCADE)
    role = models.CharField(max_length=12,
                            choices=ROLE_CHOICES, default=3)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def _get_fullname(self):
        fullname = f"{self.first_name} {self.last_name}"
        return fullname

    @property
    def fullname(self):
        return self._get_fullname()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['_class']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Assignment(models.Model):
    title = models.CharField(max_length=300)
    course = models.CharField(max_length=50)
    course_code = models.CharField(max_length=10)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignments')
    _class = models.ForeignKey(
        UserClass, on_delete=models.CASCADE, related_name='assignments')
    duration = models.DateTimeField()
    status = models.CharField(max_length=15)
    marks = models.IntegerField()

    def __str__(self):
        return self.title


class Submissions(TimestampedModel, models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='submissions')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='submissions')
    _class = models.ForeignKey(
        UserClass, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField()
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=15)
    score = models.FloatField()

    is_draft = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
