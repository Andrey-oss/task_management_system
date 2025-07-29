from django.test import TestCase
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer

# Create your tests here.

class UserSerializerTest(TestCase):
    """UserSerializer tests"""

    def setUp(self):
        self.data = {
            "username": "testuser",
            "email": "user@example.com",
            "password": "StrongPass123",
            "first_name": "Test",
            "last_name": "User"
        }
        self.another_data = {
            "username": "anotheruser",
            "email": "another@gmail.com",
            "password": "AnotherPass123",
            "first_name": "Another",
            "last_name": "User"
        }
        self.invalid_email_data = {
            "username": "anotheruser",
            "email": "another@",
            "password": "AnotherPass123",
            "first_name": "Another",
            "last_name": "User"
        }

        #self.user_obj = User.objects.create(**self.data) DEPRECATED
        # We should create user with hashed password

        self.user_obj = User.objects.create_user(**self.data)

    def test_create_account(self):
        """Serialize valid data"""

        serializer = UserSerializer(instance=self.user_obj)
        data = serializer.data

        self.assertEqual(data['id'], self.user_obj.id) # Auto created
        self.assertEqual(data['username'], self.data['username'])
        self.assertEqual(data['email'], self.data['email'])
        self.assertEqual(data['first_name'], self.data['first_name'])
        self.assertEqual(data['last_name'], self.data['last_name'])
        self.assertNotIn('password', data)

    def test_user_creation_success(self):
        """Ensure serializer creates user with valid data"""

        serializer = UserSerializer(data=self.another_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()
        self.assertEqual(user.username, self.another_data["username"])
        self.assertTrue(user.check_password(self.another_data["password"]))

    def test_account_with_the_same_unique_params(self):
        """Test create validation"""

        serializer = UserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('email', serializer.errors)

    def test_invalid_email(self):
        """Test with invalid email"""

        serializer = UserSerializer(data=self.invalid_email_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
