import requests
from django.core.management.base import BaseCommand
from spotlightcentral.models import Post
from decouple import config
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Fetch news from multiple APIs and save them as blog posts'

    def handle(self, *args, **kwargs):
        self.fetch_nyt_news()
        self.fetch_newsapi_news()

    def fetch_nyt_news(self):
        api_key = config('NYT_API_KEY')
        url = f'https://api.nytimes.com/svc/topstories/v2/home.json?api-key={api_key}'
        
        # Print the API URL for debugging
        print(f'Fetching news from NYT URL: {url}')
        
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to fetch NYT news: {response.status_code}'))
            return

        data = response.json()

        # Print the API response for debugging
        print(data)

        # Check if 'results' key is in the response
        if 'results' not in data:
            self.stdout.write(self.style.ERROR('No articles found in the NYT API response'))
            return

        for article in data['results']:
            title = article['title']
            content = article['abstract']
            author = article['byline']  # Assuming the byline as author
            source = article['section']  # Assuming the section as source
            slug = slugify(title)
            tags = article['des_facet']  # Assuming 'des_facet' contains tags
            image = article['multimedia'][0]['url'] if article['multimedia'] else None  # Assuming 'multimedia' contains images

            if not Post.objects.filter(slug=slug).exists():
                post = Post.objects.create(
                    title=title,
                    slug=slug,
                    body=content,
                    author_id=1,  # Assuming a default author ID
                    status=Post.Status.PUBLISHED,
                    source=source,
                    image=image  # Add this line
                )
                post.tags.add(*tags)  # Add tags to the post
                self.stdout.write(self.style.SUCCESS(f'Successfully added NYT post: {title}'))

    def fetch_newsapi_news(self):
        api_key = config('NEWS_API_KEY')
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
        
        # Print the API URL for debugging
        print(f'Fetching news from NewsAPI URL: {url}')
        
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to fetch NewsAPI news: {response.status_code}'))
            return

        data = response.json()

        # Print the API response for debugging
        print(data)

        # Check if 'articles' key is in the response
        if 'articles' not in data:
            self.stdout.write(self.style.ERROR('No articles found in the NewsAPI response'))
            return

        for article in data['articles']:
            title = article['title']
            content = article['description']
            author = article['source']['name']  # Assuming the source name as author
            source = article['source']['name']  # Assuming the source name as source
            slug = slugify(title)
            tags = [tag['name'] for tag in article.get('tags', [])]  # Assuming 'tags' contains tags
            image = article['urlToImage']  # Assuming 'urlToImage' contains the image URL

            if not Post.objects.filter(slug=slug).exists():
                post = Post.objects.create(
                    title=title,
                    slug=slug,
                    body=content,
                    author_id=1,  # Assuming a default author ID
                    status=Post.Status.PUBLISHED,
                    source=source,
                    image=image  # Add this line
                )
                post.tags.add(*tags)  # Add tags to the post
                self.stdout.write(self.style.SUCCESS(f'Successfully added NewsAPI post: {title}'))