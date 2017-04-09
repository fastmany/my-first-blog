from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import post
from .forms import postform
from django.shortcuts import redirect

def post_list(request):
    posts = post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post_de = get_object_or_404(post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post_de})

def post_new(request):
    if request.method == "POST":
        form = postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = postform()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post_de = get_object_or_404(post, pk=pk)
    if request.method == "POST":
        form = postform(request.POST, instance=post_de)
        if form.is_valid():
            post_de = form.save(commit=False)
            post_de.author = request.user
            post_de.published_date = timezone.now()
            post_de.save()
            return redirect('post_detail', pk=post_de.pk)
    else:
        form = postform(instance=post_de)
    return render(request, 'blog/post_edit.html', {'form': form})