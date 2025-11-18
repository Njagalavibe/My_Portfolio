from django.urls import path
from . import views

urlpatterns = [
    # Home page - lists all blog posts
    path('', views.BlogPostsView.as_view(), name='home'),
    
    # Post detail page - with engagement features
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # Like/Dislike functionality
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/dislike/', views.dislike_post, name='dislike_post'),
    
    # Post management (admin only - for you)
    path('post/new/', views.BlogPostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='post_delete'),
]


  