from django.db import models
from django.utils import timezone
from django.db.models.functions import Now
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
            )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique_for_date='publish', unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='spotlightcentral_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager()       #default manager
    published = PublishedManager()   #my custom manager
    tags = TaggableManager()
    source = models.URLField(blank=True, null=True)
    image = models.ImageField(max_length=500, upload_to='images/', blank=True, null=True)

    objects = models.Manager()       #default manager
    published = PublishedManager()   #my custom manager

    class Meta:
        ordering = ['-created']
        # this is the index option to improve performance for query filtering or ordering results by this field

        indexes = [
            models.Index(fields=['-publish'], name='post_publish_idx'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'spotlightcentral:post_detail',
            args=[self.publish.year,
                  self.publish.month,
                  self.publish.day,
                  self.slug
                  ]
        )
    
    def save(self, *args, **kwargs):
        if self.status == self.Status.PUBLISHED and not self.publish:
            self.publish = timezone.now()
        super().save(*args, **kwargs)



class Comment(models.Model):
    post = models.ForeignKey(
     Post,
     on_delete= models.CASCADE,
     related_name= 'comments'   
    )

    name = models.CharField(max_length= 25)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)
    active = models.BooleanField(default= True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields= ['created'])
        ]

        def __str__(self):
            return f'comment by {self.name} on {self.post}'
