from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from feed.views import *

app_name='feed'

urlpatterns = [
    path('',FeedLV.as_view(),name='index'),
    path('create',create_feed,name='create'),
    path('user',user_feed,name='user_feed'),
    path('<int:feed_id>/update',feed_update,name='feed_update'),
    path('<int:feed_id>/delete',feed_delete,name='feed_delete'),
    path('<int:feed_id>/like',feed_like,name='feed_like'),    # Example: /blog/tag/
    path('tag/', TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', TaggedObjectLV.as_view(), name='tagged_object_list'),
]
