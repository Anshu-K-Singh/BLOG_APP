from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.


class Post(models.Model):
    # adding a status field
    class Status (models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
        
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
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
    
    # defining a default sort order 
    
    class Meta:
        ordering  = ['-publish']
        #adding database index
        indexes = [
            models.Index(fields =['-publish'])
        ]
    
    def __str__(self):
        return self.title