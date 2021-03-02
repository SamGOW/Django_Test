from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from authentication.forms import UserForm, writeBlogs, UpdateUserForm, commentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authentication.models import User, Blogs, Comments
import random
# Create your views here.

def index(request):

    blogs = Blogs.objects.all()


    return render(request, 'index.html', {"blogs_all":blogs})

@login_required
def checkLogin(request):
    return HttpResponse("You are logged in")

def register(request):
    register = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        print('debug1')
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            dob = user_form.cleaned_data.get('date_of_birth')
            email = user_form.cleaned_data.get('email')
            print('debug1.1')
            profile_pic = user_form.cleaned_data.get('profile_pic')
            userIDV = random.randint(0, 999999)
            print('debug1.2')
            user = User.objects.create_user(userID=userIDV,username=username, date_of_birth=dob, email=email, profile_pic=profile_pic, password=password)
            if 'profile_pic' in request.FILES:
                print('found it')
                user.profile_pic = request.FILES['profile_pic']
            user.save()
            register = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'signup.html', 
    {'user_form': user_form,
    'registered': register}) 

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponse("Successfully logged in!!")
            else:
                return HttpResponse("Your Account was inactive. ")
            
        else:
            print("Login Fail")
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html') 

def user_logout(request):
    logout(request),
    return HttpResponse('Successfully logged out')

@login_required
def writeBlogsV(request):
    if request.method == 'POST':
        blogs_form = writeBlogs(request.POST)
        print('debug1')
        if blogs_form.is_valid():
            title = blogs_form.cleaned_data.get('title')
            thumbnail = blogs_form.cleaned_data.get('thumbnail')
            blog = blogs_form.cleaned_data.get('blog')
            owner = User.objects.get(username=request.user.username)
            blogs = Blogs.objects.create(owner=owner,title=title, blog=blog, thumbnail=thumbnail)
            if 'thumbnail' in request.FILES:
                print('found it')
                blogs.thumbnail = request.FILES['thumbnail']
            blogs.save()
        else:
            print(blogs_form.errors)
    else:
        blogs_form = writeBlogs()
    return render(request, 'writeBlogHTML.html', 
    {'blogs_form': blogs_form}) 

def viewBlog(request, blog_id):
    authorV = User.objects.get(username = request.user.username)
    blog = Blogs.objects.get(id = blog_id)
    print('halo')
    CommentList = ["bl"]
    CommentList.clear()
    CommentsOnBlog = Comments.objects.all()
    for x in CommentsOnBlog:
        if x.blogName == blog:
            CommentList.append(x)

    CommentFormsss = commentForm()
    if request.method == 'POST':
        CommentFormsss = commentForm(request.POST)
        if CommentFormsss.is_valid():
            commentV = CommentFormsss.cleaned_data.get('comment')
            ThatComment = Comments.objects.create(comment = commentV, blogName = blog, author = authorV)
            ThatComment.save()

    return render(request, 'viewBlog.html', {'blog_var':blog, 'CommentBox':CommentFormsss, 'Comments':CommentList})

#def addComment(request):


"""def editProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            usernameV = user_form.cleaned_data.get('username')
            passwordV = user_form.cleaned_data.get('password')
            dobV = user_form.cleaned_data.get('date_of_birth')
            emailV = user_form.cleaned_data.get('email')
            profile_picV = user_form.cleaned_data.get('profile_pic')
            user = User.objects.get(username = request.user.username)
            user.update_user(username=usernameV, password=passwordV, dob=dobV, email=emailV, profile_pic=profile_picV)
            print('done')
            return HttpResponse('affirmitive')
    else:
        user_form = UserForm()
    return render(request, 'profile.html', {'user_form':user_form})"""

def editProfile(request):
    userbase = User.objects.get(username = request.user.username)
    form = UpdateUserForm(instance=userbase)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=userbase)
        if form.is_valid():
            form.save();
            print("Yes?")

    return render(request, 'profile.html', {'user_form':form})

def viewProfile(request):
    user = User.objects.get(username = request.user.username)
    return render(request, 'viewProfile.html', {'user':user})