from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from articles import services
from articles.forms import ArticleCreateForm, ArticleCommentForm
from articles.models import Article
from articles.utils import AllowOnlyAuthorMixin, ArticlesListMixin, CategoriesMixin


class HomePageView(CategoriesMixin, ArticlesListMixin, ListView):
    def get_queryset(self):
        return services.find_published_articles()


class ArticleCategoryView(CategoriesMixin, ArticlesListMixin, ListView):
    slug_url_kwarg = "category_slug"
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        return services.find_articles_of_category(category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_category_slug"] = self.kwargs["category_slug"]
        return context


class ArticleTagView(CategoriesMixin, ArticlesListMixin, ListView):
    slug_url_kwarg = "category_slug"
    allow_empty = False

    def get_queryset(self):
        tag = self.kwargs["tag"]
        return services.find_articles_with_tag(tag)


class ArticleSearchView(CategoriesMixin, ArticlesListMixin, ListView):
    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return services.find_articles_by_query(query)


class ArticleDetailView(CategoriesMixin, DetailView):
    model = Article
    slug_url_kwarg = "article_slug"
    context_object_name = "article"
    template_name = "articles/article.html"

    def get_object(self):
        article = super().get_object()
        article = services.get_article_by_slug(article.slug)
        services.increment_article_views_counter(article.slug)
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ArticleCommentForm()
        article_slug = self.kwargs["article_slug"]
        context["comments"] = services.find_comments_to_article(article_slug)
        context["comments_count"] = len(context["comments"])
        article = context["article"]
        if self.request.user in article.users_that_liked.all():
            context["user_liked"] = True
        context["liked_comments"] = services.find_article_comments_liked_by_user(
            article_slug, self.request.user
        )
        return context


class ArticleCreateView(LoginRequiredMixin, CategoriesMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = "articles/article_create.html"
    login_url = reverse_lazy("login")

    def get_form_kwargs(self):
        kwargs = super(ArticleCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ArticleUpdateView(AllowOnlyAuthorMixin, UpdateView):
    model = Article
    fields = ["title", "category", "tags", "preview_text", "preview_image", "content"]
    slug_url_kwarg = "article_slug"
    login_url = reverse_lazy("login")
    template_name = "articles/article_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class ArticleDeleteView(AllowOnlyAuthorMixin, DeleteView):
    model = Article
    context_object_name = "article"
    slug_url_kwarg = "article_slug"
    success_url = reverse_lazy("home")


class ArticleCommentView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request, article_slug):
        form = ArticleCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = get_object_or_404(Article, slug=article_slug)
            comment.author = request.user
            comment.save()
            return redirect(reverse("article-details", args=[article_slug]))


class ArticleLikeView(View):
    def post(self, request, article_slug):
        user_id = request.user.id
        likes_count = services.toggle_article_like(article_slug, user_id)
        return JsonResponse({"likes_count": likes_count})


class CommentLikeView(View):
    def post(self, request, comment_id):
        user_id = request.user.id
        likes_count = services.toggle_comment_like(comment_id, user_id)
        return JsonResponse({"comment_likes_count": likes_count})
