from django.contrib import admin
from . models import Author,Post,Comment


class PostAdmin(admin.ModelAdmin):
    list_filter = ("author","date")
    list_display = ("title","date","author")
    prepopulated_fields = {"slug":("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment_user","post")

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment,CommentAdmin)