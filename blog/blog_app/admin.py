from django.contrib import admin
from .models import Blogs, Tags, BlogComments, BlogTags, BlogLikes, BlogCommentLikes

admin.site.register(Blogs)
admin.site.register(Tags)
admin.site.register(BlogComments)
admin.site.register(BlogTags)
admin.site.register(BlogLikes)
admin.site.register(BlogCommentLikes)
