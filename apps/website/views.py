from django.shortcuts import render
from .models import NavigationItem, Banner, ServiceOverview, Branch, GalleryImage, Preference, NewsCoverage, PageModel, FooterMenuItem
from apps.order.models import Products, Service
from django.db.models import Prefetch
from django.http import JsonResponse
from apps.blog.models import Post


def landing_page(request):
    # Fetch all top-level navigation items with their child items prefetched
    top_level_items = NavigationItem.objects.filter(parent__isnull=True).prefetch_related('children')

    banner = Banner.objects.filter(is_active=True).first()
    service_overview = ServiceOverview.objects.filter(is_active=True)
    branches = Branch.objects.filter(is_active=True)
    gallery = GalleryImage.objects.filter(is_active=True)

    preference = Preference.objects.filter(is_active=True).first()

    products = Products.objects.all()
    services = Service.objects.all()
    blogs = Post.objects.filter(is_published=True)
    news_coverage = NewsCoverage.objects.all()
    footer_items = FooterMenuItem.objects.filter(is_active=True)

    return render(request, 'index.html', {
        'navigation_items': top_level_items,
        'banner': banner,
        'service_overview': service_overview,
        'branches': branches,
        'gallery': gallery,
        'preference': preference,
        'products': products,
        'services': services,
        'news_coverage': news_coverage,
        'blogs': blogs,
        'footer_items': footer_items,
    })


def page_view(request, slug):
    
    top_level_items = NavigationItem.objects.filter(parent__isnull=True)
    preference = Preference.objects.filter(is_active=True).first()

    page_data = PageModel.objects.get(slug=slug)

    return render(request, 'page_view.html', {'page_data': page_data, 'navigation_items':top_level_items, 'preference':preference})


def filter_images(request):
    category = request.GET.get('category')
    if category == 'all':
        images = GalleryImage.objects.all()
    else:
        images = GalleryImage.objects.filter(category=category)
    
    data = [{'image': image.image.url} for image in images]
    return JsonResponse(data, safe=False)