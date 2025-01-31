from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import CustomUser
from courses.models import Category, Course


class SearchTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(phone_number='admin', password='password', role='admin')
        self.user1 = CustomUser.objects.create_user(phone_number='1234567890', password='password', role='student')
        self.user2 = CustomUser.objects.create_user(phone_number='0987654321', password='password', role='professor')

        self.category1 = Category.objects.create(name='Programming', description='Learn programming')
        self.category2 = Category.objects.create(name='Math', description='Learn Mathematics')

        self.course1 = Course.objects.create(
            name='Python Basics',
            master=self.user2,  # Professor as course owner
            category=self.category1,
            description='Introduction to Python',
            price=100.00,
            startDate='2023-01-01'
        )
        self.course2 = Course.objects.create(
            name='Algebra 101',
            master=self.user2,
            category=self.category2,
            description='Basic Algebra course',
            price=50.00,
            startDate='2023-02-01'
        )

    def test_search_users(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/search/users/', {"query": "1234567890"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['phone_number'], '1234567890')

    def test_search_categories(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/search/categories/', {"query": "Programming"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Programming')

    def test_search_courses(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/search/courses/', {"query": "Python"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Python Basics')
