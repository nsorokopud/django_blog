# Generated by Django 4.0.1 on 2022-02-16 13:46

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("taggit", "0004_alter_taggeditem_content_type_alter_taggeditem_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=256, unique=True)),
                ("slug", models.SlugField(max_length=256, unique=True)),
                ("preview_text", models.TextField(max_length=512)),
                (
                    "preview_image",
                    models.ImageField(blank=True, null=True, upload_to="articles/preview_images/"),
                ),
                ("content", ckeditor_uploader.fields.RichTextUploadingField()),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_published", models.BooleanField(db_index=True, default=False)),
                ("views_count", models.IntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Articles",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ArticleCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                ("slug", models.CharField(db_index=True, max_length=256, unique=True)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="ArticleComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="articles.article"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "users_that_liked",
                    models.ManyToManyField(
                        related_name="users_that_liked_comment", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.AddField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="articles.articlecategory",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="users_that_liked",
            field=models.ManyToManyField(
                blank=True, related_name="users_that_liked", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
