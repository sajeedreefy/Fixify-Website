
from django.urls import path, include
from apps.website.views import landing_page, page_view, filter_images
urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('page/<slug>/', page_view, name='page_view'),
    path('filter-images/', filter_images, name='filter_images'),
]
