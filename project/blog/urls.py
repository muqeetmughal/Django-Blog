
from os import name
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.Homepage.as_view(), name="home"),
    path('category/<slug>', views.CategoryArticles.as_view(),
         name="category_articles"),
    path('article/<slug>', views.SingleArticle.as_view(), name="article_detail"),
    # path('categories/', views.AllCategories.as_view(), name="all_categories"),
    path('search/', views.SearchArticles.as_view(), name="search"),
    path('subscribe/', views.AddNewsLetter.as_view(), name="subscribe"),
    path('addcomment/', views.AddComment.as_view(), name="add_comment"),
    
]
