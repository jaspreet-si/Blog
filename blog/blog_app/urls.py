
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('signup/',views.Signup,name='signup'),
    
    path('home/',views.blogs_listing,name='home'),
    path('blogs/<int:id>/',views.blog_detail,name='blog_detail'),
    path('comment/like/<int:comment_id>/',views.like_comment, name='like_comment'),
     path('blog/share/<int:blog_id>/',views.share_blog, name='share_blog'),
]
