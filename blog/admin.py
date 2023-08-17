from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "post_status", "created_at")
    search_fields = ("title", "content")
    list_filter = ("post_status", "created_at")
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    search_fields = ("content",)
    list_filter = ("created_at",)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
