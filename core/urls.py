from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

from core.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

# base_url = "backend/"
base_url = ""


urlpatterns = [
    path(base_url + "admin/", admin.site.urls),
    path(base_url + "api/", include("apps.urls")),
    # SWAGGER
    path(base_url + "api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI for SWAGGER:
    path(
        base_url + "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        base_url + "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": MEDIA_ROOT,
        },
    ),
]
