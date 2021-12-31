from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.db.models import Count

# Create your views here.
from django.views.generic import View
from . import models


class Homepage(View):
    def get(self, request):

        history_articles = models.Article.objects.filter()[:4]

        context = {
            'history_articles': history_articles
        }
        return render(request, "pages/home.html", context=context)


class SearchArticles(View):
    def get(self, request):

        query = request.GET.get("q")
        # articles = models.Article.objects.filter(title__unaccent__lower__trigram_similar=query) # for postgresql dataBASE
        articles = models.Article.objects.filter(title__contains=query)

        context = {
            "query": query,
            "articles": articles
        }
        return render(request, "pages/search.html", context)


class SingleArticle(View):
    def get(self, request, slug):

        article = models.Article.objects.get(slug=slug)
        context = {
            "article": article
        }
        return render(request, "pages/single_article.html", context)


class CategoryArticles(View):
    def get(self, request, slug):


        category = models.Category.objects.get(slug=slug)

        articles = category.article.filter()
        

        if request.GET.get("latest"):
            articles = articles.order_by('-posted_at')

        elif request.GET.get("most-comments"):
            articles = articles.annotate(q_count=Count('comments')).order_by('-q_count')

        elif request.GET.get("popular"):
            articles = articles.order_by('-views')

        else:
            articles = articles.order_by('-posted_at')


        context = {
            # 'categories': categories,
            'articles': articles,
            "category": category
        }
        return render(request, "pages/category_articles.html", context)


# class AllCategories(View):
#     def get(self, request):
#         context = {
#             "categories": models.Category.objects.all()
#         }
#         return render(request, "pages/allcategories.html", context)


class AddComment(View):
    def post(self, request):
        author = request.POST.get('author')
        email = request.POST.get('email')
        website = request.POST.get('url')
        comment = request.POST.get('comment')
        article = request.POST.get('article')
        article_instance = models.Article.objects.get(id=article)

        comment = models.Comment(
            name=author, email=email, website=website, text=comment, article=article_instance)
        comment.save()

        return redirect(reverse('article_detail', kwargs={'slug': article_instance.slug}))

class AddNewsLetter(View):

    def get(self, request):
        return HttpResponse("helo")

    def post(self, request):
        print("yes posted email")
        return redirect(request.path)