from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

# Create your models here.

# custom  models manager named publsihed
class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status = Post.Status.PUBLISHED)
            )
class Post(models.Model):
    # adding a status field
    class Status (models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
        
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    # many-to-one relationship
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post') 
    
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices = Status,
        default = Status.DRAFT)
    
    # the Default manager
    objects = models.Manager() 
    # custom manager
    published = PublishedManager()
    # defining a default sort order 
    
    class Meta:
        ordering  = ['-publish']
        #adding database index
        indexes = [
            models.Index(fields =['-publish'])
        ]
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug]
                       )
    
class Author(models.Model):
    name = models.CharField(max_length=255)