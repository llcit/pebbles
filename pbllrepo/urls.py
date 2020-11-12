"""pbllrepo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_view

from filebrowser.sites import site

from core.views import UpdateIndexView
from reposite.views import (
    HomeView,
    ProjectPrototypeCreateView, ProjectPrototypeDetailView,
    ProjectPrototypeUpdateView, ProjectPrototypeDeleteView,
    ProjectPrototypeListView, CloneProjectView,
    ProjectTaskDetailView, ProjectTaskCreateView,
    ProjectTaskUpdateView, ProjectTaskDeleteView,
    ProjectTaskListView, ProjectPrototypeDocumentView,
    ProjectImplementationInfoItemView, ProjectImplementationInfoItemCreateView, 
    ProjectImplementationInfoItemUpdateView, ProjectImplementationInfoItemDeleteView,
    FileUploadView, ImplementationInfoFileUploadView, TaskFileUploadView,
    ProjectFileDeleteView, TaskFileDeleteView, ImplementationFileDeleteView,
    SearchHaystackView,
    RepoPageView
)

from discussions.views import DiscussionListView, DiscussionView, PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('social_django.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),


    url(r'^$', HomeView.as_view(), name='home'),

    # project prototypes
    url(r'^prototypes/$', ProjectPrototypeListView.as_view(), name='list_prototypes'),
    url(r'^prototype/doc/(?P<pk>[-\d]+)/$', ProjectPrototypeDocumentView.as_view(), name='docview_prototype'),
    url(r'^prototype/(?P<pk>[-\d]+)/$', ProjectPrototypeDetailView.as_view(), name='view_prototype'),
    url(r'^prototype/add/$', ProjectPrototypeCreateView.as_view(), name='create_prototype'),
    url(r'^prototype/edit/(?P<pk>[-\d]+)/$', ProjectPrototypeUpdateView.as_view(), name='update_prototype'),
    url(r'^prototype/delete/(?P<pk>[-\d]+)/$', ProjectPrototypeDeleteView.as_view(), name='delete_prototype'),
    url(r'^prototype/flip/(?P<pk>[-\d]+)/$', CloneProjectView.as_view(), name='flip_prototype'),

    # tasks
    url(r'^prototype/(?P<project>[-\d]+)/task/(?P<pk>[-\d]+)/$', ProjectTaskDetailView.as_view(), name='view_task'),
    url(r'^prototype/(?P<pk>[-\d]+)/tasks/$', ProjectTaskListView.as_view(), name='view_all_tasks'),
    url(r'^prototype/(?P<project>[-\d]+)/task/add/$', ProjectTaskCreateView.as_view(), name='create_task'),
    url(r'^prototype/(?P<project>[-\d]+)/task/edit/(?P<pk>[-\d]+)/$', ProjectTaskUpdateView.as_view(), name='update_task'),
    url(r'^prototype/(?P<project>[-\d]+)/task/delete/(?P<pk>[-\d]+)/$', ProjectTaskDeleteView.as_view(), name='delete_task'),

    # implementation information
    url(r'^prototype/(?P<project>[-\d]+)/implementation-info/(?P<pk>[-\d]+)/$', ProjectImplementationInfoItemView.as_view(), name='view_implementation_item'),
    url(r'^prototype/(?P<project>[-\d]+)/implementation-info/add/$', ProjectImplementationInfoItemCreateView.as_view(), name='create_implementation_item'),
    url(r'^prototype/(?P<project>[-\d]+)/implementation-info/edit/(?P<pk>[-\d]+)/$', ProjectImplementationInfoItemUpdateView.as_view(), name='update_implementation_item'),
    url(r'^prototype/(?P<project>[-\d]+)/implementation-info/delete/(?P<pk>[-\d]+)/$', ProjectImplementationInfoItemDeleteView.as_view(), name='delete_implementation_item'),

    # site pages
    url(r'^page/(?P<pk>\w+)$', RepoPageView.as_view(), name='page_view'),


    # file handling
    url(r'^prototype/file-upload/(?P<proj_pk>[-\d]+)/$', FileUploadView.as_view(), name='upload_file'),
    url(r'^prototype/task-file-upload/(?P<task_pk>[-\d]+)/$', TaskFileUploadView.as_view(), name='upload_task_file'),
    url(r'^prototype/info-file-upload/(?P<info_pk>[-\d]+)/$', ImplementationInfoFileUploadView.as_view(), name='upload_info_file'),
    
    url(r'^prototype/project-file/delete/(?P<pk>[-\d]+)/$', ProjectFileDeleteView.as_view(), name='delete_file'),
    url(r'^prototype/task-file/delete/(?P<pk>[-\d]+)/$', TaskFileDeleteView.as_view(), name='delete_task_file'),
    url(r'^prototype/info-file/delete/(?P<pk>[-\d]+)/$', ImplementationFileDeleteView.as_view(), name='delete_info_file'),
    

    # url(r'^prototype/project-file-upload/(?P<project>[-\d]+)/$', ProjectFileUploadView.as_view(), name='upload_project_file'),
    # url(r'^prototype/task-file-upload/(?P<task>[-\d]+)/$', TaskFileUploadView.as_view(), name='upload_task_file'),

    # discussions
    url(r'^discussions/(?P<slug>[-\w]+)/$', DiscussionView.as_view(), name='discussion_select'),
    url(r'^discussions/$', DiscussionListView.as_view(), name='discussion'),
    url(r'^discussions/post/add/$', PostCreateView.as_view(), name='create_post'),
    url(r'^discussions/post/delete/$', PostDeleteView.as_view(), name='delete_post'),
    url(r'^discussions/post/(?P<pk>[-\w]+)/edit/$', PostUpdateView.as_view(), name='edit_post'),

    # haystack search
    # url(r'^search/', include('haystack.urls'), name='haystack_search'),
    url(r'^search/', SearchHaystackView.as_view(), name='haystack_search'),
    url(r'^update_index/$', UpdateIndexView.as_view(), name='haystack_update_index'),

    # administration
    url(r'^logout/$', auth_view.logout, name='logout'),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
