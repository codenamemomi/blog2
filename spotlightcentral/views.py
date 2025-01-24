from django.shortcuts import get_object_or_404,render
from .models import Post
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django .views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
# Create your views here.


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        post_list = post_list.filter(tags__in = [tag])
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        posts = paginator.page(1 if isinstance(page_number, int) else paginator.num_pages)

    return render(request, 'spotlightcentral/post/list.html', {'posts': posts,
                                                               'tag': tag
                                                               })

def post_details(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, 
                             slug=slug, 
                             publish__year=year, 
                             publish__month=month, 
                             publish__day=day)
    
    # active comment list
    comments = post.comments.filter(active = True)
    # form for user comments
    form = CommentForm()
      #list of similar post
    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(
        tags__in= post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags = Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return render(request, 'spotlightcentral/post/details.html', 
                    {
                    'post': post,
                    'form': form,
                    'comments': comments,
                    'similar_posts': similar_posts
                    }
                )
  

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'spotlightcentral/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(
        Post, 
        id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url =request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f'{cd['name']} ({cd['email']}) '
                f'recommends you read {post.title}'
                )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject = subject,
                message = message,
                from_email =None,
                recipient_list = [cd['to']]
            )
            sent = True
            # ... send email
            return render(request, 'spotlightcentral/post/share.html', {'post': post, 
                                                                        'form': form, 
                                                                        'sent': True})
        else:
            return render(request, 'spotlightcentral/post/share.html', {'post': post, 
                                                                        'form': form})
    else:
        form = EmailPostForm()
        return render(request, 'spotlightcentral/post/share.html', {'post': post, 
                                                                    'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data= request.POST)
    if form.is_valid():
        comment = form.save(commit= False)

        comment.post = post

        comment.save()
    return render(
        request, 'spotlightcentral/post/share.html',
        {'post': post,
         'form': form,
         'comment': comment}
    )
