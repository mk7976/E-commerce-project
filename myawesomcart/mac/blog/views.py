from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost


# Create your views here.
def index(request):
    AllBlog = Blogpost.objects.all()
    print(AllBlog)
    return render(request, 'blog/index.html', {"AllBlog": AllBlog})


def blogpost(request, post_id):
    Blog = Blogpost.objects.filter(post_id=post_id)
    print(Blog)
    return render(request, "blog/blogpost.html", {"Blog": Blog})
