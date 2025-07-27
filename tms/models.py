from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Completed'),
        ('UNDONE', 'Undone'),
        ('UNKNOWN', 'N/A'),
    ]

    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('hobby', 'Hobby'),
        ('sport', 'Sport'),
        ('others', 'Others'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, blank=False, null=False)
    text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='work')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.author} | {self.title} | {self.created_at} | {self.category}"

    class Meta:
        # I didn't set any ordering because it defaults to created_at
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
