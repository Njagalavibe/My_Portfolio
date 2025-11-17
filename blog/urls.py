from django.urls import path

from .views import (BlogPostsView, BlogPostDetailView,
BlogPostCreateView,
BlogPostUpdateView,
BlogPostDeleteView
)

urlpatterns = [
    path('', BlogPostsView.as_view(), name='home'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('post/new/', BlogPostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),
]