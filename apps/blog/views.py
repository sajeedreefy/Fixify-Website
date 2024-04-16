from django.shortcuts import render
from apps.blog.models import Post
from apps.website.models import NavigationItem, Preference


# Create your views here.
def list_page(request):

    top_level_items = NavigationItem.objects.filter(parent__isnull=True).prefetch_related('children')
    preference = Preference.objects.filter(is_active=True).first()
    blogs = Post.objects.filter(is_published=True)
    
    return render(request, 'blog_list.html', { 'preference': preference,'navigation_items': top_level_items, 'blogs': blogs })



def blog_details(request, slug):

    top_level_items = NavigationItem.objects.filter(parent__isnull=True).prefetch_related('children')
    preference = Preference.objects.filter(is_active=True).first()
    post = Post.objects.get(slug=slug)

    return render(request, 'blog_details.html', { 'preference': preference,'navigation_items': top_level_items,'post': post })


