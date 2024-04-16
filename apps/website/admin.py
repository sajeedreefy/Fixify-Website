from django.contrib import admin
from .models import NavigationItem, Banner, ServiceOverview, Branch, GalleryImage, PageModel, Preference, NewsCoverage, FooterMenuItem

# Register your models here.

admin.site.register(Banner)
admin.site.register(Branch)
admin.site.register(ServiceOverview)
admin.site.register(NewsCoverage)
admin.site.register(NavigationItem)
admin.site.register(GalleryImage)
admin.site.register(PageModel)
admin.site.register(Preference)
admin.site.register(FooterMenuItem)


admin.site.site_header = 'Technician Administration'

