from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from blog.feeds import LatestEntriesFeed, LatestEntriesByTagFeed
from blog.models import Entry
from sitemaps import SectionSitemap, BlogArchiveSitemap, TagSitemap

from django.contrib import admin
admin.autodiscover()

sitemaps = {
    'sections': SectionSitemap,
    'blog-archive': BlogArchiveSitemap,
    'blog-tags': TagSitemap,
    'flatpages': FlatPageSitemap,
    'blog': GenericSitemap({'queryset': Entry.objects.published(), 'date_field': 'mod_date',}),
}

urlpatterns = patterns('',
    # Django administration
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Main sections
    url(r'^activity/$', view='views.activity', name='main_activity'),
    url(r'^activity/page/(?P<page>\d+)/$',
        view='views.activity',
        kwargs={'explicit_page_request': True},
        name='activity_paged'),
    url(r'^blog/', include('blog.urls')),
    
    # RSS feeds
    url(r'^feeds/latest/$', view=LatestEntriesFeed(), name='blog_entries_rss'),
    url(r'^feeds/tags/(?P<tag_name>[-\w]+)/$', view=LatestEntriesByTagFeed(), name='blog_tagged_rss'),
    
    # Sitemap
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap'),
    
    # MetaWeblog integration
    url(r'^mw/', include('metaweblog.urls')),

    # Robots.txt
    url(r'^robots.txt$', view='views.robots', name='robots'),
    
    # Main site index
    url(r'^$', view='views.index', name='main_index'),
)

if settings.DEBUG:
    from settings import MEDIA_ROOT, ADMIN_MEDIA_ROOT
    
    urlpatterns += patterns('',
        url(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT,
            'show_indexes': True}),
        url(r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': ADMIN_MEDIA_ROOT, 'show_indexes': True}),
    )
