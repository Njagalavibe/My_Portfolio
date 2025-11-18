from django.contrib import admin

from .models import Post,Like,Comment

# Register your post here.
admin.site.register(Post)

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'get_user', 'is_verified', 'created_date']
    list_filter = ['is_verified', 'created_date']
    search_fields = ['content', 'guest_user', 'verified_user__username']

    #custom method to display either guest_user or verified_user
    def get_user(self, obj):
        return obj.guest_user if obj.guest_user else obj.verified_user.username
    get_user.short_description = 'User'

# Register Comment model with custom admin
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'session_key', 'reaction_type']
    list_filter = ['reaction_type',]
    search_fields = ['post__title', 'session_key']
