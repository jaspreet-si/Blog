from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tags(models.Model):
  tag_name=models.CharField(max_length=250,blank=True,null=True)
  created_at=models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table='Tags'

class Blogs(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  title=models.CharField(max_length=300,null=True,blank=True)
  content=models.TextField()
  likes_count=models.IntegerField(default=0)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  class Meta:
    db_table='Blogs'

class BlogTags(models.Model):
  blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
  tag=models.ForeignKey(Tags,on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  class Meta:
    db_table='Blog_Tags'
  


class BlogComments(models.Model):
  blog=models.ForeignKey(Blogs,on_delete=models.CASCADE,null=True)
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  comment=models.TextField(null=True,blank=True)
  likes_count=models.IntegerField(default=0)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  class Meta:
    db_table='Blog_Comments'


class BlogCommentLikes(models.Model):
  comment=models.ForeignKey(BlogComments,on_delete=models.CASCADE,null=True, related_name='likes')
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  created_at=models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table='Blog_Comment_Likes'
    unique_together = ('comment', 'user')

class BlogLikes(models.Model):
  blog=models.ForeignKey(Blogs,on_delete=models.CASCADE,null=True)
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  created_at=models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table='Blog_Likes'


  
