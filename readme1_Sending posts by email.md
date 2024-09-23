
# Sending Blog Post by Email in Django

## 1. Creating the Email Form

First, define a form in `forms.py` to collect user input: their name, email, the recipient’s email, and optional comments.

```python
from django import forms

# A form for users to share blog posts via email
class EmailPostForm(forms.Form):
    # Sender's name (max 25 characters)
    name = forms.CharField(max_length=25)
    # Sender's email (validated as a proper email)
    email = forms.EmailField()
    # Recipient's email (validated as a proper email)
    to = forms.EmailField()
    # Optional comments section (uses a TextArea widget for multi-line input)
    comments = forms.CharField(required=False, widget=forms.Textarea)
```

## 2. Handling the Form in the View

In `views.py`, write the `post_share` view to handle the form and send an email when the form is submitted. The view also processes GET requests to show the form.

```python
from django.core.mail import send_mail  # Import Django's email sending function
from django.shortcuts import get_object_or_404, render
from .models import Post  # Import the Post model
from .forms import EmailPostForm  # Import the form we created

def post_share(request, post_id):
    # Retrieve the blog post by its ID; return 404 if not found or not published
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    # Variable to check if the email has been successfully sent
    sent = False

    # Check if the request is a POST (form submission)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)  # Create the form with submitted data
        if form.is_valid():  # If all form data is valid
            cd = form.cleaned_data  # Extract the validated data from the form
            post_url = request.build_absolute_uri(post.get_absolute_url())  # Build the full URL for the post

            # Create the email subject using the sender's name and the post title
            subject = f"{cd['name']} recommends you read {post.title}"

            # Create the email body with the post link and the sender's comments (if any)
            message = f"Read {post.title} at {post_url}

{cd['name']}'s comments: {cd['comments']}"

            # Send the email using Django's send_mail function
            # Arguments: subject, message, sender's email, recipient's email
            send_mail(subject, message, cd['email'], [cd['to']])

            # Set the sent flag to True to indicate the email was successfully sent
            sent = True
    else:
        # If the request is not a POST, create an empty form for the user to fill
        form = EmailPostForm()

    # Render the form and the result (whether the email was sent or not)
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
```

## 3. Configuring Email Backend

To send emails, Django requires email backend settings. Add the following configuration to `settings.py`.

```python
# Configure Django to send emails via an SMTP server (e.g., Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Specify the email backend
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server for Gmail
EMAIL_PORT = 587  # Use port 587 for secure transmission
EMAIL_USE_TLS = True  # Enable TLS (Transport Layer Security)
EMAIL_HOST_USER = 'your_email@gmail.com'  # Your Gmail account
EMAIL_HOST_PASSWORD = 'your_password'  # Your Gmail password
```

## 4. Defining the URL Pattern

In `urls.py`, add a URL pattern that maps to the `post_share` view.

```python
from django.urls import path
from . import views

# Add a new URL pattern for sharing posts by email
urlpatterns = [
    # The URL includes the post ID and routes to the post_share view
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
```

## 5. Creating the Template

Create the `share.html` template to display the form and confirmation message after the email is sent.

```html
<h2>Share "{{ post.title }}" by email</h2>

<!-- Display the form for users to fill out and submit -->
<form method="post">
    {{ form.as_p }}  <!-- Renders the form fields as paragraph elements -->
    {% csrf_token %}  <!-- Include CSRF token for security -->
    <button type="submit">Send email</button>  <!-- Submit button for the form -->
</form>

<!-- If the email was successfully sent, display a confirmation message -->
{% if sent %}
    <p>Your email has been sent!</p>
{% endif %}
```

## Summary of Workflow

1. **Form Rendering**: The form is displayed to the user to enter details like their name, email, the recipient's email, and comments.
2. **Form Submission**: When the user submits the form, it's validated, and if valid, Django constructs and sends an email.
3. **Email Sending**: The email contains the post title, link, and any comments, and is sent to the recipient via the configured SMTP server.
4. **Feedback**: After the email is sent, the user is shown a confirmation message on the page.
