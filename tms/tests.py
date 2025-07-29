from django.test import TestCase
from django.contrib.auth.models import User
from tms.serializers import TaskSerializer, TaskDetailSerializer
from tms.models import Task
from datetime import datetime
from django.utils.timezone import make_aware

class TaskModelTest(TestCase):
    """Tests for Task model"""

    def setUp(self):
        """Setting up the environment
        
        1. Create user with credentials: tester:1234
        """

        self.user = User.objects.create_user(username='tester', password='1234')

    def test_create_full_task(self):
        deadline = make_aware(datetime(2025, 12, 31, 23, 59))
        task = Task.objects.create(
            author=self.user,
            title="My Task",
            text="Test task",
            status="IN_PROGRESS",
            category="personal",
            deadline=deadline,
            password="secret"
        )

        self.assertEqual(task.title, "My Task")
        self.assertEqual(task.status, "IN_PROGRESS")
        self.assertEqual(task.category, "personal")
        self.assertEqual(task.author.username, "tester")
        self.assertEqual(task.deadline, deadline)

    def test_default_task_values(self):
        task = Task.objects.create(
            author=self.user,
            title="My Task",
        )

        self.assertEqual(task.title, "My Task")
        self.assertEqual(task.status, "TODO")
        self.assertEqual(task.category, "work")
        self.assertEqual(task.author.username, "tester")

    def test_title_is_required(self):
        with self.assertRaises(Exception):
            Task.objects.create(author=self.user, title=None)

    def test_author_is_required(self):
        with self.assertRaises(Exception):
            Task.objects.create(text="Some text")

class TaskSerializerTest(TestCase):
    """Tests for task serializator"""

    def setUp(self):
        """
        Setting up the environment:

        1. Create user with credentials: tester:1234
        2. Create Task with some information 
        """

        self.user = User.objects.create_user(username='tester', password='1234')
        self.task = Task.objects.create(
            author=self.user,
            title='Test Task',
            text='Do something',
            status='TODO',
            deadline=make_aware(datetime(2025, 12, 31, 12, 0)),
            password='supersecret'
        )

    def test_serialize_task(self):
        serializer = TaskSerializer(instance=self.task)
        data = serializer.data

        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['status'], 'TODO')
        self.assertEqual(data['author_name'], 'tester')
        self.assertNotIn('password', data)  # write only, read the password is not allowed!

    def test_deserialize_task(self):
        payload = {
            'title': 'New Task',
            'text': 'Something to do',
            'status': 'IN_PROGRESS',
            'deadline': '2025-12-31T12:00:00Z',
            'password': 'mypassword'
        }

        serializer = TaskSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated = serializer.validated_data
        self.assertEqual(validated['title'], 'New Task')
        self.assertEqual(validated['password'], 'mypassword') # Without encryption
