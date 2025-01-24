from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
 

register = template.Library()

@register.simple_tag(name='spotlight')
def total_posts():
    """Returns the total count of published posts."""
    return Post.published.count()


@register.inclusion_tag('spotlightcentral/post/hot_gist.html')
def show_hot_gist(count=4):
    hot_gist = Post.published.order_by('-publish')[:count]
    return {'hot_gist': hot_gist}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_text(text):
    return mark_safe(markdown.markdown(text))