from django_filters import rest_framework as filters
from accounts.models import CustomUser
from courses.models import Course, Category

class UserFilter(filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = {
            'phone_number': ['icontains'],
            'email': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
        }

class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'category__name': ['icontains'],
            'price': ['exact', 'gte', 'lte'],
        }

class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
        }
