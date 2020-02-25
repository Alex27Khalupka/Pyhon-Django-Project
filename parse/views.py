from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from .models import Article

def index(request):
	articles_list = Article.objects.order_by('-date')
	return render(request, 'parse/list.html', {'articles_list': articles_list})

def detail(request, article_id):
	try:
		a = Article.objects.get(id = article_id)
	except:
		raise Http404("Page not found")

	# latest_comments_list = a.comment_set.order_by('-id')[:10]
	return render(request, 'parse/detail.html', {'article': a})
	# , 'latest_comments_list': latest_comments_list})
