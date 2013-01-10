from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^quiz/$', 'quiz.views.index'),
    url(r'^quiz/new_quiz/$', 'quiz.views.new_quiz'),
    url(r'^quiz/(?P<quiz_id>\d+)/new_question/$', 'quiz.views.new_question'),
    url(r'^quiz/(?P<question_id>\d+)/question/$', 'quiz.views.question'),
    url(r'^quiz/(?P<question_id>\d+)/submit/$', 'quiz.views.submit'),
    url(r'^quiz/answer/(?P<guess_id>\d+)/$', 'quiz.views.answer'),
    url(r'^quiz/(?P<quiz_id>\d+)/score_report/$', 'quiz.views.score_report'),
    url(r'^', 'quiz.views.index')

    # url(r'^unesco/', include('unesco.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
