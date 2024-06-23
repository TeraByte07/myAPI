from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from posts.models import Author

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class CustomUser(AbstractUser):
    is_author_requested = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

@receiver(post_save, sender=CustomUser)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def create_or_update_author(sender, instance, created, **kwargs):
    if instance.is_author:
        author, created = Author.objects.get_or_create(user=instance)
        author.first_name = instance.first_name
        author.last_name = instance.last_name
        author.bio = instance.bio
        author.website = instance.website
        author.save()
    elif not instance.is_author:
        Author.objects.filter(user=instance).delete()
