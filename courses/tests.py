from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from courses.models import Category, Course, CourseContent, Comment, Purchase

User = get_user_model()


class CategoryTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(phone_number='admin', password='password', role='admin')
        self.category_data = {'name': 'Programming', 'description': 'Learn programming'}

    def test_create_category_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post('/courses/categories/', self.category_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.get().name, 'Programming')

    def test_update_category_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        category = Category.objects.create(name='Programming', description='Learn programming')

        updated_data = {'name': 'Advanced Programming'}
        response = self.client.patch(f"/courses/categories/{category.id}/", updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Advanced Programming')

    def test_delete_category_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        category = Category.objects.create(name='Programming', description='Learn programming')

        response = self.client.delete(f"/courses/categories/{category.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CourseTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(phone_number='admin', password='password', role='admin')
        self.professor_user = User.objects.create_user(phone_number='professor', password='password', role='professor')
        self.category = Category.objects.create(name='Programming', description='Learn programming')
        self.course_data = {
            'name': 'Python Basics',
            'master': self.professor_user.id,
            'category': self.category.id,
            'description': 'Introduction to Python',
            'price': 100.00,
            'startDate': '2023-01-01'
        }

    def test_create_course_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post('/courses/create/', self.course_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.get().name, 'Python Basics')

    def test_update_course_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        course = Course.objects.create(
            name='Python Basics',
            master=self.professor_user,
            category=self.category,
            description='Introduction to Python',
            price=100.00,
            startDate='2023-01-01'
        )

        updated_data = {'name': 'Advanced Python'}
        response = self.client.patch(f'/courses/{course.id}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.name, 'Advanced Python')

    def test_delete_course_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        course = Course.objects.create(
            name='Python Basics',
            master=self.professor_user,
            category=self.category,
            description='Introduction to Python',
            price=100.00,
            startDate='2023-01-01'
        )

        response = self.client.delete(f'/courses/{course.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CourseContentTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(phone_number='admin', password='password', role='admin')
        self.professor_user = User.objects.create_user(phone_number='professor', password='password', role='professor')
        self.category = Category.objects.create(name='Programming', description='Learn programming')
        self.course = Course.objects.create(
            name='Python Basics',
            master=self.professor_user,
            category=self.category,
            description='Introduction to Python',
            price=100.00,
            startDate='2023-01-01'
        )
        self.course_content_data = {
            'course': self.course.id,
            'content_type': 'text',
            'title': 'Introduction',
            'textContent': 'Welcome to the course'
        }

    def test_create_course_content_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post('/courses/contents/', self.course_content_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseContent.objects.get().title, 'Introduction')

    def test_update_course_content_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        course_content = CourseContent.objects.create(
            course=self.course,
            content_type='text',
            title='Introduction',
            textContent='Welcome to the course'
        )

        updated_data = {'title': 'Introduction to python'}
        response = self.client.patch(f'/courses/contents/{course_content.id}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_content.refresh_from_db()
        self.assertEqual(CourseContent.objects.get().title, 'Introduction to python')

    def test_delete_course_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        course_content = CourseContent.objects.create(
            course=self.course,
            content_type='text',
            title='Introduction',
            textContent='Welcome to the course'
        )

        response = self.client.delete(f'/courses/contents/{course_content.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTests(APITestCase):
    def setUp(self):
        self.student_user = CustomUser.objects.create_user(phone_number='student', password='password', role='student')
        self.professor_user = User.objects.create_user(phone_number='professor', password='password', role='professor')
        self.category = Category.objects.create(name='Programming', description='Learn programming')
        self.course = Course.objects.create(
            name='Python Basics',
            master=self.professor_user,
            category=self.category,
            description='Introduction to Python',
            price=100.00,
            startDate='2023-01-01'
        )
        self.comment_data = {
            'course': self.course.id,
            'text': 'Great course!'
        }

    def test_create_comment_as_student(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.post('/courses/comments/', self.comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.get().text, 'Great course!')


class PurchaseTests(APITestCase):
    def setUp(self):
        self.student_user = CustomUser.objects.create_user(phone_number='student', password='password', role='student')
        self.professor_user = User.objects.create_user(phone_number='professor', password='password', role='professor')
        self.category = Category.objects.create(name='Programming', description='Learn programming')
        self.course = Course.objects.create(
            name='Python Basics',
            master=self.professor_user,
            category=self.category,
            description='Introduction to Python',
            price=100.00,
            startDate='2023-01-01'
        )

    def test_get_purchase_as_student(self):
        self.client.force_authenticate(user=self.student_user)

        self.client.post(f'/courses/purchase/{self.course.id}/')

        response = self.client.get(f'/courses/purchase/{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.get().amount_paid, 100.00)

    def test_create_purchase_as_student(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.post(f'/courses/purchase/{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Purchase.objects.get().amount_paid, 100.00)
