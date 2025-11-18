from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Post model
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
    body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    
    # Like/Dislike methods
    def get_like_count(self):
        """Returns total number of likes for this post"""
        return self.likes.filter(reaction_type='like').count()
    
    def get_dislike_count(self):
        """Returns total number of dislikes for this post"""
        return self.likes.filter(reaction_type='dislike').count()
    
    def get_user_reaction(self, session_key):
        """Check if current session user has reacted to this post"""
        try:
            like = self.likes.get(session_key=session_key)
            return like.reaction_type
        except Like.DoesNotExist:
            return None
    
    def has_user_reacted(self, session_key):
        """Check if user has already reacted"""
        return self.get_user_reaction(session_key) is not None
    
    # Comment methods
    def get_comment_count(self):
        """Returns total number of comments"""
        return self.comments.count()
    
    def get_verified_comment_count(self):
        """Returns number of verified comments"""
        return self.comments.filter(is_verified=True).count()
    
    def get_recent_comments(self, limit=5):
        """Get most recent comments"""
        return self.comments.all().order_by('-created_date')[:limit]
    
    # Properties for easy template access
    @property
    def like_count(self):
        return self.get_like_count()
    
    @property
    def dislike_count(self):
        return self.get_dislike_count()
    
    @property
    def comment_count(self):
        return self.get_comment_count()


# Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    # For authenticated user
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    # For anonymous user
    guest_name = models.CharField(max_length=100, blank=True, null=True)    
    guest_email = models.EmailField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})

    
    def __str__(self):
        if self.guest_name:
            return f"Comment by {self.guest_name} on {self.post.title}"
        elif self.user:
            return f"Comment by {self.user.username} on {self.post.title}"
        else:
            return f"Comment by Anonymous on {self.post.title}"

# Like model
class Like(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)  # To track anonymous users
    reaction_type = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # Added missing field

    class Meta:
        unique_together = ['post', 'session_key']  # Ensure one reaction per session

    def __str__(self):
        return f"{self.reaction_type} on {self.post.title} by {self.session_key}"