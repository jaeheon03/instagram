from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Feed(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    likes = models.ManyToManyField(User, related_name='liked_feeds', blank=True)
    created_at= models.DateTimeField("CREATED DATE", auto_now_add=True)
    modify_dt = models.DateTimeField("UPLOAD DATE", auto_now_add=True)
    slug=models.SlugField("SLUG",unique=True,allow_unicode=True,help_text='one word for title alias',blank=True)
    tags=TaggableManager(blank=True)
    class Meta:
        ordering=('-modify_dt',)

    def __str__(self) -> str:
        return self.title

class Image(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    feed=models.ForeignKey(Feed, on_delete=models.CASCADE)
    image_url = ProcessedImageField(upload_to='feed/%Y/%m', processors=[ResizeToFill(300, 400)])