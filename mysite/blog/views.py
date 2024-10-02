from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
# Create your views here.

"""def post_list(request):
    #posts = Post.published.all()
    post_list = Post.published.all()
    # PAgination with 3 posts per page
    paginator = Paginator(post_list, 3)# Retrieve all published posts from the Post model

    page_number  = request.GET.get('page', 1)
    posts = paginator.page(page_number)

    return render(request, "blog/post/list.html", {"posts": posts})
"""

class PostListView(ListView):
    #Alternative post list view
    
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = "blog/post/list.html"
     


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)    
    # list of active comments for this post
    comments = post.comments.filter(active = True)
    #form for the users to comment
    form = CommentForm()
    
    
    """emailpostform = EmailPostForm()

    if request.method == "POST":
        print(request.POST)
        emailpostform = EmailPostForm(request.POST)
        if emailpostform.is_valid():

            cd = emailpostform.cleaned_data
            print(cd)
"""
    return render(request, "blog/post/detail.html",
                  {"post": post, 'form': form, 'comments': comments},
                  )

def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )
    sent = False

    if request.method == "POST":
        #from was submitted
        form  = EmailPostForm(request.POST)
        if form.is_valid():
            #form fields passed the validation
            cd = form.cleaned_data
            #send email .....
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"

            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments : {cd['comments']}"
            )

            send_mail(subject, message, cd["email"], [cd['to']])

            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        "blog/post/share.html",
        {'post': post,'form' : form, 'sent' : sent}
    )


# Comment view

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
        )
    comment = None
    # A comment was posted
    form = CommentForm(data = request.POST)
    if form.is_valid():
        # create a comment object without saving it to the database
        comment = form.save(commit = False)
        # assign the post to the comment
        comment.post  = post
        # save the comment in the database
        comment.save()
    
    return render(
        request,
        "blog/post/comment.html",
        {
            'post' : post,
            'form' : form,
            'comment' : comment
        }
        )