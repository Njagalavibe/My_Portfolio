from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView   
from django.urls import reverse_lazy 

from .models import Post

class BlogPostsView(ListView):
    model = Post        
    template_name = 'home.html'

class BlogPostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

# Additional views for creating, updating, and deleting posts can be added as needed.

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