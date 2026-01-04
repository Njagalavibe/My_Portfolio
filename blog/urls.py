from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    #  PUBLIC PAGES
    #home page
    path('', views.home, name='home'),
    #blogs page
    path('blog/', views.blogs_page, name='blogs_page'),
    # single blog post view
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    # projects page
    path('projects/', views.projects_page, name='projects_page'),
    # single project view
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    # about page
    path('about/', views.about, name='about'),
    
    # Interaction URLs (TODO: Update to use slug)
    path('post/<int:pk>/like/', views.like_blog_post, name='like_blog_post'),
    path('post/<int:pk>/dislike/', views.dislike_blog_post, name='dislike_blog_post'),

    # ADMIN PAGES (Protected - only you can access) 
    # Post management
    # Admin URLs (TODO: Update to use slug)
    path('post/new/', views.BlogPostCreateView.as_view(), name='blog_post_new'),
    path('post/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='blog_post_edit'),
    path('post/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),
]

  
    
    
   