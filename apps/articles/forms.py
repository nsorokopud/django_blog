from django import forms

from articles.models import Article, ArticleComment
from articles.services import create_article


class ArticleCreateForm(forms.ModelForm):
    preview_text = forms.TextInput()

    class Meta:
        model = Article
        fields = ["title", "category", "tags", "preview_text", "preview_image", "content"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ArticleCreateForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        super(ArticleCreateForm, self).save(commit=False, **kwargs)

        article = create_article(
            title=self.cleaned_data["title"],
            author=self.request.user,
            preview_text=self.cleaned_data["preview_text"],
            content=self.cleaned_data["content"],
            category=self.cleaned_data["category"],
            tags=self.cleaned_data["tags"],
            preview_image=self.cleaned_data["preview_image"],
        )
        return article


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ["text"]
