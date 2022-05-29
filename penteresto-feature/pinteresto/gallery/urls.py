from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = 'gallery'
urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('tags/', tags_list, name='tags_list'),
    path('tag/create/', Tagcreate.as_view(), name='tag_create'),
    path('tags/<str:title>', tags_detail, name='tags_detail'),
    path('post/new/', post_new, name='post_new'),
    path('post/<int:pk>', detail, name='detail'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('like/<int:pk>', like_post, name='like_post'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

