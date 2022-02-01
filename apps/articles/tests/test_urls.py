from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from articles.views import HomePageView, ArticleDetailView
from articles.models import Article, ArticleCategory


class TestViews(TestCase):
    def setUp(self):
        self.test_user = User(username="test_user", email="test@test.com")
        self.test_user.set_password("12345")
        self.test_user.save()

        self.test_category = ArticleCategory.objects.create(title="cat1", slug="cat1")
        self.test_article = Article.objects.create(
            title="a1",
            slug="a1",
            category=self.test_category,
            author=self.test_user,
            preview_text="text1",
            content="content1",
            is_published=True,
        )

    def test_homepage_url_is_resolved(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func.view_class, HomePageView)

    def test_article_details_page_url_is_resolved(self):
        url = reverse("article-details", args=[self.test_article.slug])
        self.assertEquals(resolve(url).func.view_class, ArticleDetailView)