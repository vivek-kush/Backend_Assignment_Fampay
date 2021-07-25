import requests
import json

from .models import Video

from background_task import background

YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search/'
YOUTUBE_SEARCH_API_KEY = 'AIzaSyBg22N2eiN_wmchvj9TO4L7xCw4vnRI5Yc'
MAX_DATA_SIZE = 1000

@background
def fetch_vedeos_data():
    
    formatted_videos_data = []

    params = {
        "part": 'snippet',
        "maxResults":10,
        "q":'football',
        "key": YOUTUBE_SEARCH_API_KEY,
    }

    response = requests.get(YOUTUBE_SEARCH_URL,params=params)

    videos_data = response.json()
    
    if('error' in videos_data) :
        print(videos_data.get('error', {}).get('message'))
        return 
    
    videos_data = videos_data.get('items') or []

    if videos_data:
        formatted_videos_data = get_formatted_videos_data(videos_data)
    
    existing_video_ids = get_existing_video_ids()

    for video_data in formatted_videos_data:
        video_id = video_data.get('video_id')
        if video_data.get('video_id') not in existing_video_ids:
            insert_video = Video(**video_data)
            insert_video.save()
            existing_video_ids.add(video_id)

    if len(existing_video_ids) > MAX_DATA_SIZE:
        old_vides_ids = get_old_video_ids(len(existing_video_ids) - MAX_DATA_SIZE)
        if old_vides_ids:
            Video.objects.filter(video_id__in=old_vides_ids).delete()


def get_formatted_videos_data(videos_data):
    
    formatted_videos_data = []

    for video_data in videos_data:
        snippet_data = video_data.get('snippet') or {}
        default_thumbnail_data = snippet_data.get('thumbnails', {}).get('default')
        videos_format_data = {
            'video_id': video_data.get('id', {}).get('videoId'),
            'title': snippet_data.get('title'),
            'published_datetime': snippet_data.get('publishedAt'),
            'description': snippet_data.get('description'),
            'thumbnail_url': default_thumbnail_data.get('url')
        }

        formatted_videos_data.append(videos_format_data)

    return formatted_videos_data

def get_existing_video_ids():

    existing_videos = Video.objects.all()
    existing_video_ids = set(video.video_id for video in existing_videos)
    return existing_video_ids

def get_old_video_ids(limit):
    old_videos = Video.objects.all().order_by('published_datetime')[:limit]
    old_video_ids = set(video.video_id for video in old_videos)
    return list(old_video_ids)