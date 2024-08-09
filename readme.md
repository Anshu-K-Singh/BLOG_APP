# BLOG APPLICATION

#####  set up the project first 
startporject = mysite
startapp = blog

### add model ```post``` in the 'blog' app
First, we will define a Post model that will allow us to store blog posts in the database
take a look at the fields of this model:
• title: This is the field for the post title.
• slug: This is a SlugField field that translates into a VARCHAR column in the SQL database. A 
slug is a short label that contains only letters, numbers, underscores, or hyphens. A post with 
the title Django Reinhardt: A legend of Jazz could have a slug like django-reinhardt-legend-jazz. 
• body: This is the field for storing the body of the post.


```python
from django.db import models

class post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    
    
    def __str__(self):
        return self.title
```

###### adding date and time field
Each post will be published 
at a specific date and time. Therefore, we need a field to store the publication date and time. We also 
want to store the date and time when the Post object was created and when it was last modified.

at first we will add a publish attribute then created and updated attributes respectively 

```python

    from django.utils import timezone 
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
```
<mark>
`auto_now=True` updates the field value everytime the instance is saved while,
`auto_now_add = True` sets the field value only when the instance is created.

Utilizing the auto_now_add and auto_now datetime fields in your Django models is highly 
beneficial for tracking the creation and last modification times of objects.
</mark>

### defining a default `sort order` and  `adding database index` 

 ```python
    class Meta:
        ordering  = ['-publish']
        indexes = [
            models.Index(fields = ['-publish'])
        ]

```


We indicate 
descending order by using a hyphen before the field name, `-publish`

adding `databse index` is essential for improving query performance (and because we have sorted it according to publish datetime than the we will often wuery pists by publish)


activate the blog app in settings.py 

<mark> blog.apps.BlogConfig will allow to customize the app's configuration instead of using simple 'blog' in settings </mark>

#### adding a `Status field`

A common functionality for blogs is to save posts as a draft until ready for publication. We will add a 
status field to our model that will allow us to manage the status of blog posts. We will be using the 
Draft and Published statuses for posts.


```python 
# adding a status field
    class Status (models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    status = models.CharField(
        max_length=2,
        choices = Status,
        default = Status.DRAFT)

```

#### many-to-one relationship

The  Django  authentication  framework  comes  in  the  django.contrib.auth 
package and contains a User model. To define the relationship between users and posts, we will use 
the AUTH_USER_MODEL setting, which points to auth.User by default.

```python 
from django.conf import settings
author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post')
```

We use related_name to specify the name of the reverse relationship, from User to Post. This will 
allow us to access related objects easily from a user object by using the user.blog_posts notation. 
We will learn more about this later.

###### creating and applying migrations
to see the sql query
```
python manage.py sqlmigrate blog 0001
```