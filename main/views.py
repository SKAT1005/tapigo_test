from urllib.parse import urlparse, parse_qs

from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render
from django.views import generic, View

from .forms import CommentForm
from .models import Post, Comment


class PostListView(generic.ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list'


class PostDetail(View):
    def get(self, request, pk):
        comment_form = CommentForm
        post = Post.objects.get(id=pk)
        return render(request, 'post_detail.html', context={'comment_form': comment_form, 'post': post})

    def post(self, request, pk):
        comment_form = CommentForm(request.POST)
        pst = Post.objects.get(id=pk)
        url = request.build_absolute_uri()
        parsed_url = urlparse(url)
        comment_id = int(parsed_url.query[3:])
        if comment_form.is_valid():
            new_comment = Comment.objects.create(**comment_form.cleaned_data)
            if comment_id:
                Comment.objects.get(id=comment_id).comment.add(new_comment)
            else:
                pst.comments.add(new_comment)
                pst.save()
            return HttpResponseRedirect(f'/post/{pk}')
        return render(request, 'post_detail.html', context={'comment_form': comment_form, 'post': pst})


