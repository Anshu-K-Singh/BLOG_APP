
# Creating a Comment System in Django

## 1. Creating a Model for Comments
The first step is to define a model to store the comments. This model will include fields like the commenter's name, email, the content of the comment (body), and the post to which the comment is related. 

```python
from django.db import models
from .models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
```

## 2. Registering the Comment Model in Admin
To manage the comments via Django's admin interface, you register the `Comment` model. You can customize what fields are displayed in the list view and which fields can be filtered and searched.

```python
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
```

## 3. Creating a Form for Comments
Next, create a form based on the `Comment` model using Django’s `ModelForm`. This form will be used to collect and validate user input for the comments.

```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
```

## 4. Handling the Form in Views
In the view, we will display the post detail along with its associated comments, and also handle the submission of the comment form. If the form is valid, the comment will be saved and associated with the post.

```python
from django.shortcuts import get_object_or_404, render
from .models import Post, Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})
```

## 5. Adding Comments to the Post Detail View
To display the comments and the comment form on the post detail page, you need to update the `post_detail` view to include both the comments and the form.

```python
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})
```

## 6. Creating the Comment Form Template
We create a template for the comment form to be included in the post detail view and to handle form submission.

```html
<h2>Add a new comment</h2>
<form action="{% url 'blog:post_comment' post.id %}" method="post">
    {{ form.as_p }}
    {% csrf_token %}
    <p><input type="submit" value="Add comment"></p>
</form>
```

## 7. Displaying Comments in the Post Detail Template
To display the list of comments and the comment form, modify the `post/detail.html` template.

```html
<h1>{{ post.title }}</h1>
<p>{{ post.body|linebreaks }}</p>

<h2>Comments</h2>
{% for comment in comments %}
    <p>{{ comment.name }} said: {{ comment.body }}</p>
    <p>Posted on {{ comment.created }}</p>
{% endfor %}

{% include 'blog/post/includes/comment_form.html' %}
```

## Summary
1. **Model Creation**: Define a `Comment` model that associates a comment with a blog post.
2. **Admin Management**: Register the `Comment` model in Django’s admin site for easy management.
3. **Form Creation**: Build a form to submit new comments using Django’s `ModelForm`.
4. **View Handling**: Handle comment form submission in the view and associate it with the appropriate post.
5. **Templates**: Render the list of comments and the form in the post detail page, allowing users to add new comments.
