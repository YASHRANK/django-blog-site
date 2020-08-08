from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect , get_object_or_404
from django.urls import reverse

from .models import Post, Comment
from taggit.models import Tag
from .forms import CreateUserForm , CreatPostForm , CommentForm

from django.contrib.auth.models import Group , User
from django.db.models import Q

from django.contrib.auth.decorators import login_required # django builtin decorator 
from .decorators import  unauthenticated_user

from django.contrib.auth import authenticate, login, logout # authentication functions 
from django.contrib import messages
from .utils import get_random_profile_pic , send_subscriber_mail

from django.core.paginator import Paginator
# Create your views here.

def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:4]
    
    context = {'posts':posts }
    return render(request, 'blog_app/home.html', context)




@unauthenticated_user
def sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save() #return username 

            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, f'Account created for {user}')
            
            login(request, user)
            return redirect('blog:main_page')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
               

    context = {'form':form}
    return render(request, 'blog_app/sign_up.html', context)


@unauthenticated_user
def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'logged in as {username}')
            return redirect('blog:main_page')
        else:
            messages.info(request, 'Username or Password is invalid !')
            print('message executed')

    context= {}
    return render(request , 'blog_app/login_user.html', context)


@login_required(login_url='blog:login_user')
def logout_user(request):
    logout(request)
    messages.info(request, "Logged Out")
   
    return redirect('blog:home')


def connect_mail(request):
    if request.method == "POST":
        c_email = request.POST.get('c_email')
        send_subscriber_mail(c_email)
    return HttpResponse("You have subscribed")
        

@login_required(login_url='blog:login_user')
def blog_detail(request, slug):
    post = Post.objects.get(slug=slug)

    profile_pic = get_random_profile_pic()
    
    comments = Comment.objects.filter(post = post)
    
    context = {'post':post , 'profile_pic':profile_pic, 'comments':comments}
    return render(request, 'blog_app/detailblog.html', context)


@login_required(login_url='blog:login_user')
def main_page(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    #show most common tags
    common_tags = Post.tags.most_common()[:5]

    paginator = Paginator(posts, 6) #show 6 objects of posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'posts':posts, 'page_obj':page_obj, 'common_tags':common_tags}
    return render(request, 'blog_app/main_page.html', context)


def search(request):
    q = request.GET.get('q')
    posts = None
    if q:
        posts = Post.objects.filter(title__icontains = q)
        print(posts)
    context = {'posts': posts}
    return render(request, 'blog_app/search.html', context)

@login_required(login_url='blog:login_user')
def my_blogs(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    total_blogs = posts.count()
    active_blogs =posts.filter(is_published=True).count()
    print(total_blogs, active_blogs)

    context = {'posts':posts, 'total_blogs':total_blogs, 'active_blogs':active_blogs}
    return render(request, 'blog_app/my_blogs.html',context)




@login_required(login_url='blog:login_user')
def write_post(request):
    form = CreatPostForm()
    if request.method == "POST":
        form = CreatPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            print('blog saved')
            return redirect('blog:main_page')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")            
    

    context = {'form':form,}
    return render(request, 'blog_app/create_post.html', context)


@login_required(login_url='blog:login_user')
def update_post(request , id):

    current_post = Post.objects.get(id=id)
    form = CreatPostForm(instance=current_post)
    if request.method == 'POST':
        form = CreatPostForm(request.POST, instance=current_post)
        if form.is_valid():
            form.save()
            messages.success(request, "post updated")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    context = {'form':form}

    return render(request , 'blog_app/update_post.html', context)


@login_required(login_url='blog:login_user')
def publish_post(request , id):
    Post.objects.filter(id=id).update(is_published=True)
    return HttpResponseRedirect('/blog/my_blogs/')



@login_required(login_url='blog:login_user')
def delete_post(request , id):

    post = Post.objects.get(id=id).delete()
    messages.info(request, f'Post deleted !')

    return HttpResponseRedirect('/blog/my_blogs/')


@login_required(login_url='blog:login_user')
def comment(request, id):
    post = get_object_or_404(Post, id=id)

    # Processing POST requests
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('blog:blog_detail', slug=post.slug)
    else:
        for msg in comment_form.error_messages:
            messages.error(request, f"{msg}: {form.error_messages[msg]}")
    
    return redirect('blog:blog_detail', slug=post.slug)
