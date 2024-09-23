Here’s the markdown code, formatted like the previous markdown files I provided:


# Blog Application in Django

## 1. Building a Blog Application
To begin with, we start by creating a simple blog application with models, views, and templates.

### Creating a Post Model
The `Post` model defines the structure of our blog posts with fields such as `title`, `slug`, `body`, and `publish` date.

```python
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title
```

### Registering the Post Model in Admin
To manage blog posts via Django’s admin interface, we register the `Post` model.

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish']
    prepopulated_fields = {'slug': ('title',)}
```

### Creating Views and Templates
We need to create views to handle displaying a list of posts and individual post details.

#### Views:
```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
```

#### Templates:
```html
<!-- blog/post/list.html -->
{% for post in posts %}
    <h2>{{ post.title }}</h2>
    <p>{{ post.body|truncatewords:30 }}</p>
    <a href="{{ post.get_absolute_url }}">Read more</a>
{% endfor %}
```

---

## 2. Sending Blog Posts by Email
Allow users to share blog posts via email.

### Creating the Email Form
Create a form to collect the sender's and recipient's email addresses along with a comment.

```python
from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
```

### Sending the Email
In the view, handle form submission and send the email using Django’s `send_mail` function.

```python
from django.core.mail import send_mail

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
```

### Configuring Email Settings
In `settings.py`, configure the email backend using Gmail or any other SMTP server.

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
```

---

## 3. Enhancing the Blog Application
Add pagination, SEO-friendly URLs, and more features to the blog.

### Pagination
To add pagination, modify the view to use Django’s `Paginator`:

```python
from django.core.paginator import Paginator

def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)  # 3 posts per page
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request, 'blog/post/list.html', {'posts': posts})
```

---

## 4. Creating a Comment System
Allow users to comment on posts.

### Comment Model
Define a `Comment` model that links to the `Post` model.

```python
from django.db import models
from .models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
```

### Creating the Comment Form
Create a form for submitting new comments.

```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
```

### Handling Comments in the View
Display comments and handle form submission in the `post_detail` view.

```python
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})
```

```

This is the full code for all the parts before class-based views, formatted similarly to the previous markdown files you requested. You can now save or use it as needed. Let me know if you need further adjustments!