from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number field must be set'))
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('professor', 'Professor'),
        ('student', 'Student'),
    ]

    username = None
    email = models.EmailField(_('email address'), blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['role', 'password']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class AbstractProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)

    class Meta:
        abstract = True


class AdminProfile(AbstractProfile):
    username = models.CharField(max_length=100, unique=True, blank=True)


class ProfessorProfile(AbstractProfile):
    specialty = models.CharField(max_length=100, blank=True, null=True)
    workbook = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_courses = models.ManyToManyField('courses.Course', related_name='professors', blank=True)


class StudentProfile(AbstractProfile):
    username = models.CharField(max_length=20, unique=True, blank=True)
    national_code = models.CharField(max_length=10, blank=True, null=True)
    purchased_courses = models.ManyToManyField('courses.Course', related_name='students', blank=True)
