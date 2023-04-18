from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Users


class ClientRegistrationTest(APITestCase):

    def test_registration_1(self):
        """
        Test client registration
        """
        url = '/api/v1/registration/client/'
        data = {
            'email': 'user@example.com',
            'password': 'string',
            'first_name': 'string',
            'last_name': 'string',
            'sex': 'string',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Users.objects.count(), 1)
        self.assertEqual(Users.objects.get().email, 'user@example.com')

    def test_registration_2(self):
        url = '/api/v1/registration/client/'
        data = {
            'email': 'user@example.com',
            'password': 'string',
            'first_name': 'string',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_registration_3(self):
        url = '/api/v1/registration/client/'
        data = {
            'email': 'rrrrr',
            'password': 'string',
            'first_name': 'string',
            'last_name': 'string',
            'sex': 'string',
            'role': 'string'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # def test_auth_1(self):
    #     url = '/api/v1/users/auth/'
    #     data = {'email': 'aaaaa', 'password': 'aaaaaa'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
    #
    # def test_auth_2(self):
    #     url = '/api/v1/users/auth/'
    #     data = {'email': 'user@example.com'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)



