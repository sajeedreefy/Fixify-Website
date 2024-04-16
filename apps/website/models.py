from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class NavigationItem(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    link = models.CharField(max_length=200, verbose_name=_('Link'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('Parent'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))

    class Meta:
        ordering = ['position', ]

    def __str__(self):
        return self.title


class Banner(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    sub_title = models.CharField(max_length=200, verbose_name=_('Sub Title'))
    hero_image = models.ImageField(upload_to='assets')
    button_link = models.CharField(max_length=200)


class ServiceOverview(BaseModel):
    title = models.CharField(max_length=300, verbose_name=_('Title'))
    sub_title = models.CharField(max_length=400, verbose_name=_('Sub Title'))
    position = models.IntegerField(default=0, verbose_name=_('Position'), )

    class Meta:
        ordering = ['position', ]

    def __str__(self):
        return self.title


class GalleryImage(BaseModel):
    image = models.ImageField(upload_to='gallery', verbose_name=_('Gallery Image'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    category = models.CharField(max_length=20, verbose_name=_('Category'))

    class Meta:
        ordering = ['position', ]


class NewsCoverage(BaseModel):
    headline = models.CharField(max_length=300, verbose_name=_('Headline'))
    media_logo = models.ImageField(upload_to='media_logo', verbose_name=_('Media Logo'))
    context = models.TextField(max_length=500, verbose_name=_('News Context'))
    news_link = models.CharField(max_length=300, verbose_name=_('News Link'), blank=True)

    def __str__(self):
        return self.headline


class Branch(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('Branch Name'))
    address = models.CharField(max_length=300, verbose_name=_('Address'), blank=True)
    phone = models.CharField(max_length=300, verbose_name=_('Phone'), blank=True)

    def __str__(self):
        return self.name


class PageModel(BaseModel):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=250
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True
    )

    content = RichTextField(
        verbose_name=_('Content')
    )

    feature_image = models.ImageField(
        upload_to='page_images',
        verbose_name=_('Featured Image'),
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(PageModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page', args=[str(self.slug)])


class Preference(BaseModel):
    logo = models.ImageField(upload_to='assets')
    address = models.CharField(max_length=200, verbose_name=_('Address'))
    email = models.CharField(max_length=200, verbose_name=_('Email'), blank=True)
    phone = models.CharField(max_length=200, verbose_name=_('Phone'), blank=True)
    whatsapp = models.CharField(max_length=200, verbose_name=_('Whatsapp'), blank=True)

    facebook_url = models.CharField(max_length=200, verbose_name=_('Facebook Url'), blank=True)
    linkedin_url = models.CharField(max_length=200, verbose_name=_('Linkedin Url'), blank=True)
    instagram_url = models.CharField(max_length=200, verbose_name=_('Instagram Url'), blank=True)


class FooterMenuItem(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    link = models.CharField(max_length=200, verbose_name=_('Link'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('Parent'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))

    class Meta:
        ordering = ['position', ]

    def __str__(self):
        return self.title
