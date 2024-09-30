from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.core.mail import send_mail

from django.core.paginator import Paginator

# def home(request):
#     return render(request,'home.html')

def login(request):
  if request.method=="GET":

       return render(request,'login.html')
       
  else:
        username=request.POST['username']
       
        password=request.POST['password']

        try:
            if '@' in username:
               
                user=auth.authenticate(email=username,password=password)
            else:
                user=auth.authenticate(username=username,password=password)
        except:
            messages.warning(request,'Invalid Credential')
            return redirect('signup')
        
        if user is not None:
            auth.login(request,user)
            return redirect('home')

        else:
            messages.warning(request,'invalid username or password ')
            return redirect('login')

 
def Signup(request):
  if request.method=='GET':
        return render(request,'signup.html')
  else:
       
        username =request.POST['username']
        email=request.POST['email']
        password=request.POST['password']    
         

       
        
        if User.objects.filter(email=email) and not User.objects.filter(username=username):

            messages.warning(request,'email already exists')
            return redirect('signup')
        elif User.objects.filter(username=username) and not User.objects.filter(email=email):
              messages.warning(request,'username already exists')
              return redirect('signup')

        elif User.objects.filter(email=email,username=username):
            messages.warning(request,'account already exists')
            return redirect('signup')
        else:
            User.objects.create_user(email=email,username=username,password=password)
            messages.success(request,'account has been created')
            return redirect('login')
      
def blogs_listing(request):
    blogs = Blogs.objects.all()
    
   
    search_query = request.GET.get('search', '')
    print('search ',search_query)
    if search_query:
        
           blogs = blogs.filter(
            Q(title__icontains=search_query) | 
            Q(blogtags__tag__tag_name__icontains=search_query)
        ).distinct()
    paginator = Paginator(blogs, 5) 
    page_number = request.GET.get('page', 1)
    page_blogs = paginator.get_page(page_number)

    return render(request, 'blogs.html', {'blogs': page_blogs, 'search_query': search_query})


def blog_detail(request, id):
    blog = get_object_or_404(Blogs, id=id)
    comments = BlogComments.objects.filter(blog=blog).order_by('-created_at')
    all_comments=[]
    for comment in comments:
        comments_detail={
            'id':comment.id,
            'user':comment.user,
            'comment':comment.comment,
        }

        if BlogCommentLikes.objects.filter(comment_id=comment.id,user=request.user).exists():
            comments_detail['isLiked']=True
        else:
            comments_detail['isLiked']=False
        all_comments.append(comments_detail)
            
    print(all_comments)
    
        
    if request.method == 'POST':
        comment_content = request.POST['comment']
        if request.user.is_authenticated:
            BlogComments.objects.create(blog=blog, user=request.user, comment=comment_content)
            messages.success(request, 'Comment added successfully.')
        else:
            messages.warning(request, 'You need to log in to comment.')
        return redirect('blog_detail', id=id)

    return render(request, 'blog_detail.html', {'blog': blog, 'comments': all_comments})

# Like functionality for comments
@login_required
def like_comment(request, comment_id):
    comment=BlogComments.objects.get(id=comment_id)
    if not BlogCommentLikes.objects.filter(comment=comment,user=request.user).exists():
        BlogCommentLikes.objects.create(comment=comment,user=request.user)
        comment.likes_count+=1
        comment.save()
        
    else:
        BlogCommentLikes.objects.filter(comment=comment,user=request.user).delete()
        comment.likes_count-=1
        comment.save()
    return redirect('blog_detail', id=comment.blog.id)




def share_blog(request, blog_id):
    blog = Blogs.objects.get(id=blog_id)

    if request.method == 'POST':
        recipient_email = request.POST['recipient_email']
        subject = f"Check out this blog: {blog.title}"
        message = f"Hi,\n\nI thought you might be interested in this blog:\n\n{blog.title}\n\n{blog.content}\n\nCheck it out!"
        from_email = 'example@gmail.com'  

        try:
            send_mail(subject, message, from_email, [recipient_email])
            print("successfully shared")
            messages.success(request, 'Blog shared successfully!')
        except Exception as e:
            
            messages.error(request, f"Error sharing blog: {str(e)}")
        
        return redirect('blog_detail', id=blog_id)