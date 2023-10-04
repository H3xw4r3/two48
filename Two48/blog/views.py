from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from .forms import PostForm, CommentForm, RegisterForm, LoginForm
from .models import Post, Comment


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, "blog_home.html", context)


def dashboard(request):
    post = Post.objects.get(title="Beyond the eyes")
    return render(request, 'users/dashboard.html', {'post':post})


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(f'hello {username}')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print('Success')
            return redirect('blog_home')
        else:
            messages.error(request, "Incorrect username or password")

    return render(request, 'login.html', {})


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']

            messages.success(request, f"Account created for {user}")
            return redirect('login/')
        
    context = {'form':form}
    return render(request, 'register.html', context)


@login_required
def create_post(request):
    form = PostForm()
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.category.add(1)

            return redirect('dashboard')
        else:
            return HttpResponse("Invalid")

    context = {
        'form': form,
    }
    return render(request, 'create_post.html', context)


def post_view(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                post = post,
                name = form.cleaned_data['name'],
                text = form.cleaned_data['text']
            )
            comment.save()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'post_view.html', context)


def category_view(request, category):
    #posts = Post.objects.all()

    posts = Post.objects.filter(
        category__name__contains=category
    )

    context = {
        'category' : category,
        'posts' : posts
    }

    return render(request, "category_view.html", context)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        results = Post.objects.filter(title__icontains=query)
    return render(request, 'search.html', {
        'query': query,
        'results': results
    })