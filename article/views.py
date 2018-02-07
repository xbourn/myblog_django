from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
from django.http import Http404
from django.contrib.syndication.views import Feed


def home(request):
	post_list = Article.objects.all()
	return render(request, 'home.html', {'post_list': post_list})


def detail(request, id):
	try:
		post = Article.objects.get(id=str(id))
	except Article.DoesNotExist:
		raise Http404
	return render(request, 'post.html', {'post': post})


def archives(request):
	try:
		post_list = Article.objects.all()
	except Article.DoesNotExist:
		raise Http404
	return render(request, 'archives.html', {'post_list': post_list,'error': False})


def aboutme(request):
	return render(request, 'aboutme.html')


def atag(request, tag):
	try:
		post_list = Article.objects.filter(category=tag)
	except Article.DoesNotExist:
		raise Http404
	return render(request, 'tag.html', {'post_list': post_list})


def blog_search(request):
	if 's' in request.GET:
		s = request.GET['s']
		if not s:
			return render(request, 'home.html')
		else:
			post_list = Article.objects.filter(title__icontains=s)
			if len(post_list) == 0:
				return render(request, 'archives.html', {'post_list': post_list, 'error': True})
			else:
				return render(request, 'archives.html', {'post_list': post_list, 'error': False})
	return redirect('/')


class RSSFeed(Feed):
	title = "RSSFeed - article"
	link = "/feed"
	description = "RSS Feed - blog posts"

	def items(self):
		return Article.objects.order_by('-date_time')

	def item_title(self, item):
		return item.title

	def item_pubdate(self, item):
		return item.date_time

	def item_description(self, item):
		return item.content
