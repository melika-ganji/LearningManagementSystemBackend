from django.db import models
from django.utils.timezone import now

from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CourseContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    contentFile = models.FileField(upload_to='course_contents/', blank=True, null=True)
    textContent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.name} - {self.title} ({self.content_type})"


class Course(models.Model):
    name = models.CharField(max_length=200)
    master = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'professor'})
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    startDate = models.DateField()
    studentsCount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PriceHistory(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Price for {self.course.name}: {self.price} on {self.changed_at}"


class Heading(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='headings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.phone_number} on {self.course.name}"


class Purchase(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="purchases")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="purchases")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.student.username} - {self.course.name} - {self.amount_paid}"


class RevenueReport(models.Model):
    date = models.DateField(default=now)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Revenue on {self.date}: {self.total_revenue}"
