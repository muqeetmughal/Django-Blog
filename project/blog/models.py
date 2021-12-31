from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse

import datetime
from mptt.models import MPTTModel, TreeForeignKey


class Newsletter(models.Model):

    email = models.EmailField(max_length=255, null=False, blank=False)

class Category(MPTTModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(editable=False, unique=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')



    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('category_articles', kwargs={'slug': self.slug})  # new


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        # this line below save every fields of the model instance
        super(Category, self).save(*args, **kwargs)



    # created_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(editable=False, unique=True)

    def __str__(self):
        return self.name + " | "+self.slug

    def save(self, *args, **kwargs):
        # this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        # this line below save every fields of the model instance
        super(Tag, self).save(*args, **kwargs)

class Article(models.Model):

    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    body = RichTextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, default="Uncategorized",blank=True, related_name="article")
    tags = models.ManyToManyField(Tag, default=None,blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True)

    views = models.BigIntegerField(null=True,blank=True, default=0, editable=True)

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,editable=False)

    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})  # new

    def save(self, *args, **kwargs):
        # this line below give to the instance slug field a slug name
        self.slug = slugify(self.title)
        # this line below save every fields of the model instance
        super(Article, self).save(*args, **kwargs)

class Comment(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, null=False, blank=False, default=None)
    email = models.EmailField(max_length=100, null=False, blank=False, default=None)
    website = models.CharField(max_length=100, null=True, blank=True)
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name="comments")
    # parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    
    website = models.CharField(max_length=255, null=True, blank=True)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.BooleanField(default=True)