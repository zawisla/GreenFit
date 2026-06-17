"""URL configuration for the GreenFit project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Branding for the Django admin (used to manage the plant catalogue).
admin.site.site_header = "Администрирование GreenFit"
admin.site.site_title = "GreenFit"
admin.site.index_title = "Управление каталогом растений"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("catalog/", include("catalog.urls")),
    path("", include("selector.urls")),
]

# Serve user-uploaded media files through the dev server when DEBUG is on.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
