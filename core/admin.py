from django.contrib import admin

from reposite.models import ProjectPrototype, PrototypeMetaElement, \
    ProjectTask, ProjectFile, ProjectComment, ProjectCoeditors, RepoPage, \
    TaskFile, ImplementationFile
from discussions.models import Post

class ExtraMedia:
    js = [
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/tinymce_setup.js',
    ]

class ProjectPrototypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'origin', 'active', 'featured')
    list_filter = ['creator', 'origin', 'active', 'featured']
    list_editable = ['active', 'featured']


class PrototypeMetaElementAdmin(admin.ModelAdmin):
    list_display = ('prototype_project', 'element_type', 'element_data')
    list_filter = ['prototype_project', 'element_type', 'element_data']


class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('prototype_project', 'creator',
                    'task_category', 'title', 'sequence_order')
    list_filter = ['prototype_project']
    list_editable = ['task_category', 'title', 'sequence_order']


class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'project')


class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'task')


class ImplementationFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'implementation')


class ProjectCoeditorsAdmin(admin.ModelAdmin):
    list_display = ('prototype_project', 'coeditor')
    list_filter = ['prototype_project', 'prototype_project__creator', 'coeditor']


class RepoPageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'featured', 'get_absolute_url')
    list_display_links = ('pk',)

admin.site.register(ProjectPrototype, ProjectPrototypeAdmin, Media=ExtraMedia)
admin.site.register(PrototypeMetaElement, PrototypeMetaElementAdmin)
admin.site.register(ProjectTask, ProjectTaskAdmin)

admin.site.register(ProjectFile, ProjectFileAdmin)
admin.site.register(TaskFile, TaskFileAdmin)
admin.site.register(ImplementationFile, ImplementationFileAdmin)

admin.site.register(ProjectComment)
admin.site.register(ProjectCoeditors, ProjectCoeditorsAdmin)
admin.site.register(RepoPage, RepoPageAdmin, Media=ExtraMedia)

admin.site.register(Post)
