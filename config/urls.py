from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from board.models import Post

info_dict = {
    'queryset': Post.objects.active().filter(),
    'date_field': 'created_at',
}

urlpatterns = [
    path('admin', admin.site.urls),
    # SEO 용
    path('sitemap.xml', sitemap, {'sitemaps': {'board': GenericSitemap(info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: /admin/\nDisallow: /account/\nAllow: /", content_type="text/plain")),
    path('ads.txt', lambda x: HttpResponse("google.com, pub-1987584597836949, DIRECT, f08c47fec0942fa0", content_type="text/plain")),
    path('notification', include('notification.urls')),
    path('', include('board.urls')),
    path('chatgpt', include('chatgpt.urls')),

    # 일반 로그인
    path('accounts/', include('accounts.urls')),
    # 소셜 로그인
    path('accounts/', include('allauth.urls')),

    # ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
