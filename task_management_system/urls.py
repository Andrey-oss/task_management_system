"""
URL configuration for task_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from index.views import index_view, about_view
from tms.views import CreateTask, ReadTask, UpdateTask, DeleteTask, DisplayMyTasks
from accounts.views import LoginView, RegisterView, profile_view, logout_view
from api.views import MeView, TaskViewSet

urlpatterns = [
    # Admin section
    path('admin/', admin.site.urls, name='admin'),

    # Index section
    path('', index_view, name='index'),
    path('about/', about_view, name='about'),

    # Account section
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),

    # Task section
    path('task/create/', CreateTask.as_view(), name='create_task'),
    path('task/<int:pk>/read/', ReadTask.as_view(), name='read_task'),
    path('task/<int:pk>/update/', UpdateTask.as_view(), name='update_task'),
    path('task/<int:pk>/delete/', DeleteTask.as_view(), name='delete_task'),
    path('my_tasks/', DisplayMyTasks.as_view(), name='my_tasks'),

    # API Section

    #path('api/', include('accounts.urls')),
    path('api/me/', MeView.as_view(), name='me'),
    path('api/', include("api.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
