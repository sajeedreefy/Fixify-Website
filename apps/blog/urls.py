
from django.urls import path, include
from apps.blog.views import list_page, blog_details
app_name = 'blog'
urlpatterns = [
    path('', list_page, name='list_page'),
    path('details/<slug>/', blog_details, name='blog_details'),
]
