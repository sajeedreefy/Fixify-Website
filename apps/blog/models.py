from django.db import models
from django.contrib.auth.models import User
from apps.website.models import BaseModel
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from ckeditor.fields import RichTextField

# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content =  RichTextField(verbose_name='Content')
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-create_time']

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a slug from the title and append a random string to ensure uniqueness
            self.slug = slugify(self.title) + '-' + get_random_string(length=4)
            # Check if the slug is unique, if not, regenerate until it is unique
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title) + '-' + get_random_string(length=4)
        super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return self.title