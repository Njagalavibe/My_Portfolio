from django.contrib import admin

from .models import Post, Like, Comment

# Register your post here.
admin.site.register(Post)

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'get_user', 'is_verified', 'created_date']
    list_filter = ['is_verified', 'created_date']
    search_fields = ['content', 'guest_name', 'user__username']  # FIXED: changed verified_user to user

    # custom method to display either guest_name or user
    def get_user(self, obj):
        return obj.guest_name if obj.guest_name else (obj.user.username if obj.user else "Anonymous")  # FIXED: changed verified_user to user
    get_user.short_description = 'User'

# Register Like model with custom admin
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'session_key', 'reaction_type']
    list_filter = ['reaction_type',]
    search_fields = ['post__title', 'session_key']