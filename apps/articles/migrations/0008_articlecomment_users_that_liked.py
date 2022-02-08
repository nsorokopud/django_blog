# Generated by Django 4.0.1 on 2022-02-07 17:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0007_remove_article_likes_article_users_that_liked"),
    ]

    operations = [
        migrations.AddField(
            model_name="articlecomment",
            name="users_that_liked",
            field=models.ManyToManyField(
                related_name="users_that_liked_comment", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
