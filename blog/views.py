from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView   
from django.urls import reverse_lazy 
from .models import Post, Like, Comment
from .forms import CommentForm

# Views for blog posts
class BlogPostsView(ListView):
    model = Post        
    template_name = 'home.html'

# Use the function-based post_detail (it has more features)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Ensure session exists for anonymous tracking
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # Check if user has already reacted
    user_reaction = post.get_user_reaction(session_key)
    
    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.guest_name = "Anonymous"
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    # Get comments for this post
    comments = post.comments.all().order_by('-created_date')
    
    context = {
        'post': post,
        'user_reaction': user_reaction,
        'session_key': session_key,
        'comment_form': form,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

# Create, Update, Delete views
class BlogPostCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = '__all__'

class BlogPostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

class BlogPostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

# Like/Dislike functionality
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Ensure session exists
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # Check if user already reacted
    existing_like = Like.objects.filter(post=post, session_key=session_key).first()
    
    if existing_like:
        # If already liked, remove the like (toggle)
        if existing_like.reaction_type == 'like':
            existing_like.delete()
        else:
            # If was dislike, change to like
            existing_like.reaction_type = 'like'
            existing_like.save()
    else:
        # Create new like
        Like.objects.create(post=post, session_key=session_key, reaction_type='like')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    existing_like = Like.objects.filter(post=post, session_key=session_key).first()
    
    if existing_like:
        if existing_like.reaction_type == 'dislike':
            existing_like.delete()
        else:
            existing_like.reaction_type = 'dislike'
            existing_like.save()
    else:
        Like.objects.create(post=post, session_key=session_key, reaction_type='dislike')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))