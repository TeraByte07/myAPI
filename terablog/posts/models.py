from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Author Entries"


# class Tag(models.Model):
#     caption = models.CharField(max_length=10)

#     def __str__(self):
#         return self.caption
#     class Meta:
#         verbose_name_plural = "Tag Entries"

class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    date = models.DateField(auto_now = True)
    slug = models.SlugField(unique=True, db_index = True)
    content = models.TextField(validators = [MinLengthValidator(10)])
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True, related_name="posts")
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    #tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Post Entries"

class Comment(models.Model):
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)#, related_name="review"
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)