from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy 
from .models import Post, Like, Comment, Project
from .forms import CommentForm


# PUBLIC VIEWS
# Home page view
def home(request):
    """
    Home page with custom animations and unique menu design.
    No blog posts displayed - just artistic elements and navigation.
    """
    return render(request, 'home.html')

# Blogs views
def blogs_page(request):
    """Show all published blog posts"""
    posts = Post.objects.filter(status='published').order_by('-published_date')
    return render(request, 'blogs_page.html', {'posts': posts})

# Single blog post view
def blog_detail(request, slug):
    """Show single blog post - UPDATED to use slug"""
    post = get_object_or_404(Post, slug=slug)
    # TODO: Update session-based logic to user-based
    return render(request, 'blog_detail.html', {'post': post})

# Projects views
def projects_page(request):
    """Show all projects"""
    projects = Project.objects.all().order_by('-created_date')
    return render(request, 'projects_page.html', {'projects': projects})

# Single project view
def project_detail(request, slug):
    """Show single project"""
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_detail.html', {'project': project})

# About page view
def about(request):
    """About page"""
    return render(request, 'about.html')


#  INTERACTION VIEWS 
# TODO: Update these to use slug and user-based system
# Like/Dislike functionality
def like_blog_post(request, pk):
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

def dislike_blog_post(request, pk):
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


# ADMIN VIEWS
class BlogPostCreateView(CreateView):
    model = Post
    template_name = 'blog_post_new.html'
    fields = '__all__'

class BlogPostUpdateView(UpdateView):
    model = Post
    template_name = 'blog_post_edit.html'
    fields = ['title', 'body']

class BlogPostDeleteView(DeleteView):
    model = Post
    template_name = 'blog_post_delete.html'
    success_url = reverse_lazy('home')

