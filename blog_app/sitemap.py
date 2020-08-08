from django.contrib.sitemaps import Sitemap
from blog_app.models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    