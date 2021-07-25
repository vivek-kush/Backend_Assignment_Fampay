
from .models import Video
from .serializers import VideModelSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
# Create your views here.



@api_view(['GET'])
def get_videos(request):

    videos_data = Video.objects.all().order_by('-published_datetime')
    paginator = Paginator(videos_data, 10)
    page_number = request.GET.get('page', 1) 
    videos_data = paginator.get_page(page_number)
    response = [VideModelSerializer(video_data).data for video_data in videos_data]
    return Response(response)

@api_view(['GET'])
def search_videos(request):
    search_term = request.GET.get('search_term') or ''
    page_number = request.GET.get('page', 1)
    
    videos_title_data = Video.objects.filter(title__icontains=search_term)
    videos_title_data = set(record for record in videos_title_data)
    videos_description_data = Video.objects.filter(description__icontains=search_term)
    videos_description_data = set(record for record in videos_description_data)
    all_searched_videos_data = [record for record in videos_title_data.union(videos_description_data)]
    paginator = Paginator(all_searched_videos_data, 10)
    all_searched_videos_data = paginator.get_page(page_number)
    response = [VideModelSerializer(video_data).data for video_data in all_searched_videos_data]
    return Response(response)
