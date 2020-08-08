from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User #for creatig user 
from django.utils.text import slugify
from .utils import get_random_hero, get_random_string, get_random_profile_pic


from taggit.managers import TaggableManager


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255,null=True, unique=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default=get_random_hero())
    is_published = models.BooleanField(default=False)
    tags = TaggableManager()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + get_random_string(8)
        super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.body
        
    
        
    