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

adding `databse index` is essential for 
improving query performance (and because we have sorted it according to publish datetime than the we will often wuery pists by publish)


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


## Customizing the administration site 
```python
from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author', 'publish', 'status', 'created']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ("status", "publish")
    raw_id_fields = ['author']
    #show_facets = admin.ShowFacets.ALWAYS 

```


## Queryset Managers
QuerySets are only evaluated in the following cases:
• The first time you iterate over them
• When you slice them, for instance, Post.objects.all()[:3]
• When you pickle or cache them
• When you call repr() or len() on them
• When you explicitly call list() on them
• When you test them in a statement, such as bool(), or, and, or if

## Custom Model Managers

Let’s create a custom manager to retrieve all posts that have a PUBLISHED status.

There are two ways to add or customize managers for your models: you can add extra manager methods 
to an existing manager or create a new manager by modifying the initial QuerySet that the manager 
returns. The first method provides you with a QuerySet notation like ```Post.objects.my_manager()```, 
and the latter provides you with a QuerySet notation like ```Post.my_manager.all().```
We will choose the second method to implement a manager that will allow us to retrieve posts using 
the notation ```Post.published.all().```
```python 
class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status = Post.Status.PUBLISHED)
            )
class Post(models.Model):
    # model fields
    # ...
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.


```            

 If  you  declare  any  managers  for 
your model but you want to keep the objects manager as well, you have to add it explicitly to your 
model. In the preceding code, we have added the default objects manager and the published custom 
manager to the Post model.


## Creating Post list and  detail views

in blog app views.py 

```python 
from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})

def post_detail(request, id):
    post = get_object_or_404(Post,id = id, status = Post.Status.PUBLISHED) 
    
    return render(request, "blog/post/detail.html", {"post": post})

```

urls.py

```python
from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name = 'post_list'),
    path('<int:id>/', views.post_detail, name = 'post_detail'),
    
]


mysite/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace = 'blog')),
]


```

## Using canonical URLs for the models

for this we will use get_absolute_url() method

models.py 

```python
from django.urls import reverse

#inside the post models class indent
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.id]
    )


```

edit the blog/post/list.html file and replace
```<a href="{% url 'blog:post_detail' post.id %}">```

with this

```<a href="{{ post.get_absolute_url }}">```



# Creating a SEO friendly website

for this we will be using the slug fields and publish  date
 
 the slug fields must be unique on a specific publishe date to avoid confusion 

unoque_for_date =  'publish'

##### Modifying the URL patterns


lets `modify` the URL patterns to use the publication `date` and `slug` for the `post detail URL `


 blog/urls.py
replace this
path('<int:id>/', views.post_detail, name='post_detail'),

with this

```python
path(
    '<int:year>/<int:month>/<int:day>/<slug:post>/',
    views.post_detail,
    name='post_detail'
),
```

##### modifying the views

we will change the parameters of the `post_detail` view to match the new URL parameters

``` python
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
```

##### modifying the canonical URL for posts
we also have to modify the parameters of canonical URL for blog posts to match the new URL parameters

`models.py`
```python
def get_Absolute_url(Self):
    ## -------------
     return reverse(
            'blog:post_detail', #giving the arguments in place of just id 
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
```


# Adding PAGINATION 

`post_list` view

```python 
from django.core.paginator import Paginator

 post_list = Post.publish.all()
    # PAgination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number  = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    

```

##### Creating a pagination template
templates/pagination.html

```html

<div class="pagination">
  <span class="step-links">
    {% if page.has_previous %}
      <a href="?page={{ page.previous_page_number }}">Previous</a>
    {% endif %}
    <span class="current">
      Page {{ page.number }} of {{ page.paginator.num_pages }}.
    </span>
    {% if page.has_next %}
      <a href="?page={{ page.next_page_number }}">Next</a>
    {% endif %}
  </span>
</div>

```
in list.html
```
{% include "pagination.html" with page = posts %}
```
We use with to pass additional context variables to the template.