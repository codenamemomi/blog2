from django.contrib.syndication.views import Feed
from .models import Post

class LatestPostFeed(Feed):
    title = "Latest Posts"
    link = "/"
    description = "Updates on the latest blog posts."

    def items(self):
        return Post.published.all()[:5]  # Adjust the number of posts as needed

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.get_absolute_url()
