from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = 'spotlightcentral'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('news/', views.news_list, name='news_list'),  # New URL pattern for news list
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_details, name='post_detail')
    # ... other URL patterns
]
