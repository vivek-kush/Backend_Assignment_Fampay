from django.urls import path
from . import views, tasks
from background_task.models import Task

Task.objects.all().delete()
tasks.fetch_vedeos_data(repeat=30)


urlpatterns = [
    path('videos/', views.get_videos),
    path('search/', views.search_videos),
]