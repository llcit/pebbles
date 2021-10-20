
from collections import OrderedDict
from html.parser import HTMLParser


from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from braces.views import LoginRequiredMixin
from haystack.generic_views import SearchView

from core.mixins import ListUserFilesMixin
from discussions.forms import PostReplyForm

from .models import ProjectPrototype, ProjectTask, ProjectImplementationInfo, ProjectFile, ProjectComment, RepoPage, TaskFile, ImplementationFile, TASK_CATEGORIES
from .forms import ProjectPrototypeCreateForm, ProjectPrototypeUpdateForm, TaskCreateForm, TaskUpdateForm, ImplementationInfoCreateForm,FileUploadForm, TaskFileUploadForm, ImplementationFileUploadForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        prototypes = ProjectPrototype.objects.all().filter(active=True)
        context['prototype_list'] = prototypes.filter(featured=False)
        context['prototype_featured'] = prototypes.filter(featured=True)

        try:
            context['prototypes_by_creator'] = ProjectPrototype.objects.filter(creator=self.request.user)
        except:
            pass

        languages = {}
        for i in prototypes:
            for j in i.get_languages():
                try:
                    languages[j] = languages[j] + 1
                except:
                    languages[j] = 1

        context['languages'] = languages

        return context


# Prototype views
class ProjectPrototypeDocumentView(DetailView):
    model = ProjectPrototype
    template_name = 'project_prototype_doc.html'
    context_object_name = 'project_prototype'

    def get_context_data(self, **kwargs):
        context = super(
            ProjectPrototypeDocumentView, self).get_context_data(**kwargs)
        project = self.get_object()

        """ tasks are keyed by task_category """
        tasks = OrderedDict()
        for i in TASK_CATEGORIES: tasks[i[1]] = None
        
        for i in project.tasks.all():
            try:
                tasks[i.get_task_category_display()].append(i)
            except:
                tasks[i.get_task_category_display()] = []
                tasks[i.get_task_category_display()].append(i)

        implementation_info_items = project.implementation_info.all()

        thread = ProjectComment.objects.get(project=project).thread or None
        initial_post_data = {}
        initial_post_data['creator'] = self.request.user
        initial_post_data['subject'] = 'Re: %s' % project.title
        initial_post_data['parent_post'] = thread
        form = PostReplyForm(initial=initial_post_data)

        context['tasks'] = tasks
        context['description'] = project.description
        context['thread'] = ProjectComment.objects.get(project=project).thread
        context['comments'] = thread.replies.filter(deleted=False)
        context['implementation_info_items'] = implementation_info_items
        context['postform'] = form
        try:
            context['filelisting'] = project.project_files.all()
        except:
            context['filelisting'] = None
        return context


class CloneProjectView(LoginRequiredMixin, DetailView):
    model = ProjectPrototype
    template_name = 'project_prototype_detail.html'
    context_object_name = 'project_prototype'

    def get(self, request, *args, **kwargs):
        clone = self.get_object().clone_project(self.request.user)
        if clone:
            objstr = self.get_object().title
            messages.add_message(request, messages.INFO, 'You have just flipped ' + objstr + '! You might want to rename it to give it your special stamp.')
            return HttpResponseRedirect(reverse('update_prototype', args=[clone.id]))

        return super(CloneProjectView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CloneProjectView, self).get_context_data(**kwargs)
        context['prototype_data'] = self.get_object().get_data_dict()

        return context


class ProjectPrototypeListView(TemplateView):
    template_name = 'project_prototype_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectPrototypeListView, self).get_context_data(**kwargs)
        prototypes = []
        for i in ProjectPrototype.objects.filter(active=True):
            proto = (i, i.get_data_dict())
            prototypes.append(proto)

        if self.request.user.is_staff:
            for i in ProjectPrototype.objects.filter(active=False):
                proto = (i, i.get_data_dict())
                prototypes.append(proto)

        try:
            context['prototypes_by_creator'] = ProjectPrototype.objects.filter(creator=self.request.user)
        except:
            pass
        
        languages = {}
        for i in prototypes:
            for j in i[0].get_languages():
                try:
                    languages[j] = languages[j] + 1
                except:
                    languages[j] = 1

        context['languages'] = languages
        context['prototype_list'] = prototypes
        return context


class ProjectPrototypeDetailView(DetailView):
    model = ProjectPrototype
    template_name = 'project_prototype_detail.html'
    context_object_name = 'project_prototype'

    def get_context_data(self, **kwargs):
        context = super(
            ProjectPrototypeDetailView, self).get_context_data(**kwargs)
        
        context['prototype_data'] = self.get_object().get_data()
        
        tasks = OrderedDict()
        for i in self.get_object().tasks.all():
            try:
                tasks[i.get_task_category_display()].append(i)
            except:
                tasks[i.get_task_category_display()] = []
                tasks[i.get_task_category_display()].append(i)

        # context['user_is_coeditor'] = self.get_object().coeditors.filter(coeditor=self.request.user)
        # if not context['user_is_coeditor']:
        # context['user_is_coeditor'] = self.request.user.is_staff

        context['prototype_tasks'] = tasks  # self.get_object().tasks.all()
        context['task_list'] = self.get_object().tasks.all()
        return context


class ProjectPrototypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProjectPrototype
    template_name = 'project_prototype_create_update.html'
    form_class = ProjectPrototypeCreateForm
    success_message = "Your new project looks great! Perhaps you can put your mind to the tasks :)!"

    def get_initial(self):
        """ Returns the initial data to use for forms on this view. """
        initial = self.initial.copy()
        initial['creator'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(
            ProjectPrototypeCreateView, self).get_context_data(**kwargs)
        return context


class ProjectPrototypeUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectPrototype
    template_name = 'project_prototype_create_update.html'
    context_object_name = 'project_prototype'
    form_class = ProjectPrototypeUpdateForm

    def get_initial(self):
        """ Returns the initial metadata to use for forms on this view. """
        choice_fields = self.get_object().meta_data_schema().multiple_choice_fields()

        initial = self.initial.copy()

        """ Initialize from metadata values """
        for i in self.get_object().data.all():
            if i.element_type in choice_fields:
                try:
                    initial[i.element_type].append(i.element_data)
                except:
                    initial[i.element_type] = [i.element_data]
            else:
                initial[i.element_type] = i.element_data

        return initial

    def get_context_data(self, **kwargs):
        context = super(
            ProjectPrototypeUpdateView, self).get_context_data(**kwargs)
        file_tree = {}      
        file_tree['project'] = self.request.user.uploaded_files.filter(project=self.get_object())
        file_tree['task'] = self.request.user.uploaded_task_files.filter(task__prototype_project=self.get_object())
        file_tree['implementation'] = self.request.user.uploaded_implementation_files.filter(implementation__prototype_project=self.get_object())
        context['filelisting'] = file_tree
        return context


class ProjectPrototypeDeleteView(LoginRequiredMixin, DeleteView):
    model = ProjectPrototype
    template_name = 'project_prototype_delete_confirm.html'
    context_object_name = 'project_prototype'
    success_url = reverse_lazy('list_prototypes')


# Task Views
class ProjectTaskListView(LoginRequiredMixin, DetailView):
    model = ProjectPrototype
    template_name = 'task_detail.html'

    def get_context_data(self, **kwargs):
        context = super(
            ProjectTaskListView, self).get_context_data(**kwargs)
        context['prototype_project'] = self.get_object()
        context['task_list'] = self.get_object().tasks.all()
        if context['task_list']:
            context['project_task'] = context['task_list'][0]
        # context['user_is_coeditor'] = context['prototype_project'].coeditors.filter(coeditor=self.request.user)
        # if not context['user_is_coeditor']:
        context['user_is_coeditor'] = self.request.user.is_staff
        context['implementation_items'] = self.get_object().implementation_info.all()       
        return context


class ProjectTaskDetailView(ListUserFilesMixin, DetailView):
    model = ProjectTask
    template_name = 'task_detail.html'
    context_object_name = 'project_task'

    def get_context_data(self, **kwargs):
        context = super(
            ProjectTaskDetailView, self).get_context_data(**kwargs)
        self.project = self.get_object().prototype_project
        context['prototype_project'] = self.project
        context['task_list'] = context['prototype_project'].tasks.all()
        # context['user_is_coeditor'] = context['prototype_project'].coeditors.filter(coeditor=self.request.user)
        # if not context['user_is_coeditor']:

        context['user_is_coeditor'] = self.request.user.is_staff

        return context


class ProjectTaskCreateView(LoginRequiredMixin, CreateView):
    model = ProjectTask
    template_name = 'task_create_update.html'
    context_object_name = 'project_task'
    form_class = TaskCreateForm
    project = None

    def get_initial(self):
        initial = self.initial.copy()
        try:
            self.project = ProjectPrototype.objects.get(
                pk=self.kwargs['project'])
            initial['prototype_project'] = self.project.id
            cat = self.request.GET.get('cat') or None
            initial['task_category'] = cat
        except Exception as e:
            print (e)
        return initial

    def get_context_data(self, **kwargs):
        context = super(
            ProjectTaskCreateView, self).get_context_data(**kwargs)
        context['prototype_project'] = self.project
        tasks = self.project.tasks.all()
        seq_orders = {i[0]: 0 for i in TASK_CATEGORIES}
        for i in tasks:
            if i.task_category:
                seq_orders[i.task_category] += 1
        context['sequence_orders'] = seq_orders
        context['edit_text'] = 'Add a new task to <em>' + self.project.title + '</em>'

        return context


class ProjectTaskUpdateView(LoginRequiredMixin, ListUserFilesMixin, UpdateView):
    model = ProjectTask
    template_name = 'task_create_update.html'
    context_object_name = 'project_task'
    form_class = TaskUpdateForm

    def get_context_data(self, **kwargs):
        context = super(
            ProjectTaskUpdateView, self).get_context_data(**kwargs)
        
        project = self.get_object().prototype_project
        file_tree = {}
        file_tree['project'] = self.request.user.uploaded_files.filter(project=project)
        file_tree['task'] = self.request.user.uploaded_task_files.filter(task=self.get_object())

        context['prototype_project'] = project
        context['edit_text'] = 'Modify ' + self.get_object().title + ' in project <em>' + project.title + '</em>'
        context['filelisting'] = file_tree       
        return context


class ProjectTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = ProjectTask
    template_name = 'task_delete_confirm.html'
    context_object_name = 'project_task'

    def get_success_url(self):
        return reverse('view_all_tasks', args=[self.get_object().prototype_project.id, ])


# Implementation Info Views
class ProjectImplementationInfoItemView(LoginRequiredMixin, DetailView):
    model = ProjectImplementationInfo
    template_name = 'implementation_info_detail.html'
    context_object_name = 'information_item'

    def get_context_data(self, **kwargs):
        context = super(
            ProjectImplementationInfoItemView, self).get_context_data(**kwargs)
        context['project_prototype'] = self.get_object().prototype_project
        return context


class ProjectImplementationInfoItemCreateView(LoginRequiredMixin, CreateView):
    model = ProjectImplementationInfo
    template_name = 'implementation_info_create_update.html'
    context_object_name = 'information_item'
    form_class = ImplementationInfoCreateForm

    def get_initial(self):
        initial = self.initial.copy()
        try:
            self.project = ProjectPrototype.objects.get(
                pk=self.kwargs['project'])
            initial['prototype_project'] = self.project.id
        except:
            pass

        return initial

    def get_success_url(self):
        return reverse('view_all_tasks', args=[self.object.prototype_project.id, ])

    def get_context_data(self, **kwargs):
        context = super(
            ProjectImplementationInfoItemCreateView, self).get_context_data(**kwargs)
        context['prototype_project'] = self.project
        context['edit_text'] = 'Adding a new implementation item to <em>' + self.project.title + '</em>'
        return context
        

class ProjectImplementationInfoItemUpdateView(LoginRequiredMixin, ListUserFilesMixin, UpdateView):
    model = ProjectImplementationInfo
    template_name = 'implementation_info_create_update.html'
    context_object_name = 'information_item'
    form_class = ImplementationInfoCreateForm

    def get_success_url(self):
        return reverse('view_all_tasks', args=[self.get_object().prototype_project.id, ])

    def get_context_data(self, **kwargs):
        context = super(
            ProjectImplementationInfoItemUpdateView, self).get_context_data(**kwargs)

        project = self.get_object().prototype_project
        file_tree = {}
        file_tree['project'] = self.request.user.uploaded_files.filter(project=project)
        file_tree['implementation'] = self.request.user.uploaded_implementation_files.filter(implementation=self.get_object())

        context['prototype_project'] = self.get_object().prototype_project
        context['edit_text'] = 'Modify ' + self.get_object().title + ' in project <em>' + self.get_object().prototype_project.title + '</em>'
        context['filelisting'] = file_tree
        return context


class ProjectImplementationInfoItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ProjectImplementationInfo
    template_name = 'implementation_info_delete_confirm.html'
    context_object_name = 'information_item'

    def get_success_url(self):
        return reverse('view_all_tasks', args=[self.get_object().prototype_project.id, ])


# Repo site pages
class RepoPageView(DetailView):
    model = RepoPage
    template_name = 'repo_page.html'
    context_object_name = 'page'

    def get(self, request, *args, **kwargs):
        if self.get_object().private:
            return redirect('staff_page_view', item=self.get_object().id)
        return super(RepoPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RepoPageView, self).get_context_data(**kwargs)
        context['admin_edit'] = reverse('admin:reposite_repopage_change', args=(self.get_object().id,))
        return context


# File handling
class FileUploadView(LoginRequiredMixin, CreateView):
    model = ProjectFile
    template_name = 'file_upload.html'
    form_class = FileUploadForm
    # success_url = reverse_lazy('upload_file')

    def get(self, request, *args, **kwargs):
        self.project_obj = ProjectPrototype.objects.get(pk=kwargs.get('proj_pk'))
        return super(FileUploadView, self).get(request, *args, **kwargs)

    def get_initial(self):
        project = self.request.GET.get('p', None)
        initial = self.initial.copy()
        try:
            initial['user'] = self.request.user
            initial['project'] = self.project_obj
        except:
            pass
        return initial

    def get_success_url(self):
        return reverse('upload_file', args=[self.object.project.pk])

    def get_context_data(self, **kwargs):
        context = super(FileUploadView, self).get_context_data(**kwargs)
       
        file_tree = {}
        file_tree['project'] = self.request.user.uploaded_files.filter(project=self.project_obj)
        context['filelisting'] = file_tree
        context['upload_target'] = 'Project Prototype'
        context['upload_target_object'] = self.project_obj
        context['project_obj'] = self.project_obj

        # context['upload_target'] = reverse('upload_file')
        # context['filelisting'] = self.request.user.uploaded_files.all()
        return context


class TaskFileUploadView(LoginRequiredMixin, CreateView):
    model = TaskFile
    template_name = 'file_upload.html'
    form_class = TaskFileUploadForm
    

    def get(self, request, *args, **kwargs):
        self.task_obj = ProjectTask.objects.get(pk=kwargs.get('task_pk'))
        return super(TaskFileUploadView, self).get(request, *args, **kwargs)

    def get_initial(self):
        task = self.request.GET.get('p', None)
        initial = self.initial.copy()
        try:
            initial['user'] = self.request.user
            initial['task'] = self.task_obj
        except:
            pass
        return initial

    def get_success_url(self):
        return reverse('upload_task_file', args=[self.object.task.pk ])

    def get_context_data(self, **kwargs):
        context = super(TaskFileUploadView, self).get_context_data(**kwargs)
        
        project = self.task_obj.prototype_project
        file_tree = {}
        # file_tree['project'] = self.request.user.uploaded_files.filter(project=project)
        file_tree['task'] = self.request.user.uploaded_task_files.filter(task=self.task_obj)

        context['filelisting'] = file_tree 
        context['upload_target'] = 'Task'
        context['upload_target_object'] = self.task_obj
        context['project_obj'] = project
        return context


class ImplementationInfoFileUploadView(LoginRequiredMixin, CreateView):
    model = ImplementationFile
    template_name = 'file_upload.html'
    form_class = ImplementationFileUploadForm
    success_url = reverse_lazy('upload_info_file')

    def get(self, request, *args, **kwargs):
        self.info_obj = ProjectImplementationInfo.objects.get(pk=kwargs.get('info_pk'))
        return super(ImplementationInfoFileUploadView, self).get(request, *args, **kwargs)

    def get_initial(self):
        implementation = self.request.GET.get('p', None)
        initial = self.initial.copy()
        try:
            initial['user'] = self.request.user
            initial['implementation'] = self.info_obj
        except:
            pass
        return initial

    def get_success_url(self):
        return reverse('upload_info_file', args=[self.object.implementation.pk ])

    def get_context_data(self, **kwargs):
        context = super(ImplementationInfoFileUploadView, self).get_context_data(**kwargs)
        
        project = self.info_obj.prototype_project
        file_tree = {}
        # file_tree['project'] = self.request.user.uploaded_files.filter(project=project)
        file_tree['implementation'] = self.request.user.uploaded_implementation_files.filter(implementation=self.info_obj)

        context['filelisting'] = file_tree
        context['upload_target'] = 'Implementation Information Item'
        context['upload_target_object'] = self.info_obj
        context['project_obj'] = project
        return context


class ProjectFileDeleteView(LoginRequiredMixin, DeleteView):
    model = ProjectFile
    template_name = 'project_file_delete_confirm.html'

    def get_success_url(self):
        return reverse('update_prototype', args=[self.get_object().project.pk])+ '#filebrowser'

    def get_context_data(self, **kwargs):
        context = super(ProjectFileDeleteView, self).get_context_data(**kwargs)
        context['project'] = self.get_object().project
        return context


class TaskFileDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskFile
    template_name = 'project_file_delete_confirm.html'

    def get_success_url(self):
        return reverse('view_all_tasks', args=[self.get_object().task.prototype_project.pk ])

    def get_context_data(self, **kwargs):
        context = super(TaskFileDeleteView, self).get_context_data(**kwargs)
        context['project'] = self.get_object().task.prototype_project
        return context


class ImplementationFileDeleteView(LoginRequiredMixin, DeleteView):
    model = ImplementationFile
    template_name = 'project_file_delete_confirm.html'

    def get_success_url(self):
        return reverse('view_all_tasks', args=[self.get_object().implementation.prototype_project.pk ])

    def get_context_data(self, **kwargs):
        context = super(ImplementationFileDeleteView, self).get_context_data(**kwargs)
        context['project'] = self.get_object().implementation.prototype_project
        return context


# Search views
class SearchHaystackView(SearchView):
    def get_queryset(self):
        queryset = super(SearchHaystackView, self).get_queryset()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(SearchHaystackView, self).get_context_data(*args, **kwargs)
        
        return context

