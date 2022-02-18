from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required
from ckeditor_uploader.views import upload


urlpatterns = [
    path("ckeditor/upload/", login_required(upload), name="ckeditor_upload"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("articles.urls")),
    path("", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("admin/", admin.site.urls))
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.append(path("__djangoblog__/", admin.site.urls))
