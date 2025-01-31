from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class AccountTests(APITestCase):

    def setUp(self):
        self.admin_data = {
            "phone_number": "1234567890",
            "password": "adminpass",
            "role": "admin",
            "name": "Admin",
            "lastName": "User",
            "username": "adminuser"
        }
        self.professor_data = {
            "phone_number": "1234567891",
            "password": "professorpass",
            "role": "professor",
            "name": "Professor",
            "lastName": "User",
            "specialty": "Computer Science",
            "workbook": "Sample Workbook",
            "description": "Experienced professor"
        }
        self.student_data = {
            "phone_number": "1234567892",
            "password": "studentpass",
            "role": "student",
            "name": "Student",
            "lastName": "User",
            "username": "studentuser",
            "national_code": "1234567892"
        }

    def test_admin_registration(self):
        response = self.client.post("/accounts/register/", self.admin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone_number=self.admin_data["phone_number"]).exists())

    def test_professor_registration(self):
        response = self.client.post("/accounts/register/", self.professor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone_number=self.professor_data["phone_number"]).exists())

    def test_student_registration(self):
        response = self.client.post("/accounts/register/", self.student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone_number=self.student_data["phone_number"]).exists())

    def test_login(self):
        self.client.post("/accounts/register/", self.admin_data, format='json')

        login_data = {
            "phone_number": self.admin_data["phone_number"],
            "password": self.admin_data["password"]
        }

        response = self.client.post("/accounts/login/", login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_admin_profile_retrieval(self):

        register_response = self.client.post("/accounts/register/", self.admin_data, format='json')
        login_data = {
            "phone_number": self.admin_data["phone_number"],
            "password": self.admin_data["password"]
        }

        response1 = self.client.post("/accounts/login/", login_data, format='json')
        access_token = response1.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')

        response = self.client.get(f'/accounts/profile/admin/{register_response.data["user"]["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.admin_data["name"])