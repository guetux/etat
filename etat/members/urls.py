from django.conf.urls import patterns, url

urlpatterns = patterns('etat.members.views',
    url(r'^$',
        'member_list',
        name='member_list'
    ),
    url(r'^(?P<m_id>\d+)/$',
        'member_view',
        name='member_view',
    ),
    url(r'^(?P<m_id>\d+)/edit/$',
        'member_edit',
        name='member_edit'
    ),
)
