# forms_py

from datetime import datetime

from django import forms
from django.forms import ClearableFileInput

# from filebrowser.widgets import ClearableFileInput

from .models import ProjectPrototype, PrototypeMetaElement, ProjectTask, ProjectImplementationInfo, ProjectFile, TaskFile, ImplementationFile
from .schema import PrototypeMetadataForm


class ProjectPrototypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectPrototypeForm, self).__init__(*args, **kwargs)
        
        # Assign the local model fields to the 'basic' group. 
        basefields = self.Meta.fields
        for i in basefields:
            self.fields[i].label = 'Basic Properties'
            self.fields[i].label_suffix = self.Meta.label_suffixes[i]


        # New groups can be created/adjusted here if needed
        # E.g, self.fields['description'].label = 'Description'

        # Now set up the fields derived from the schema. 
        metadata_form = PrototypeMetadataForm()
        for i, j in metadata_form.fields.items():
            self.fields[i] = j
        
        # Assign the subject area field to the 'basic' group
        self.fields['subject'].label = 'Basic Properties'

        # Specify the display order of the fields
        self.order_fields(['title', 'description', 'driving_question', 'subject', 'active', 'icon', 'creator', 'origin', 'publisher', 'publish_date', 'contributors'])


    class Meta:
        model = ProjectPrototype

        """ Base model fields (i.e., these descriptors are NOT specified in schema but with the model) """
        fields = ('title', 'active','description', 'icon', 'creator', 'origin', 'publisher', 'publish_date', 'contributors', 'driving_question')
        
        """ Label groups identify related groups. These are assigned in init or in PrototypeMetadataForm """
        label_groups = ['Basic Properties', 'Language', 'Instructional Context', 'Language Proficiency', 'World Readiness Standards', '21st Century Skills']

        """ Label  suffixes are used to label each item within a label group """
        label_suffixes = {
            'title': 'Project Title',
            'icon': 'Project Icon',
            'creator': 'Author',
            'origin': 'Derived from?',
            'description': 'Description',
            'publisher': 'Publisher',
            'publish_date': 'Publish Date',
            'contributors': 'Contributors',
            'active': 'Public',
            'driving_question': 'Driving Question'
        }

        """
        Note: Making origin field hidden to prevent changing/creating a flip.
        Doing so will inherently reclone: remove the current object and
        make a new one from the specified clone. "Recloning" is equivalent to
        deleting the current object and cloning a new one from the desired prototype.
        We won't handle that complexity here for the sake of clarity.
        """

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': ClearableFileInput(attrs={'class': 'form-control'}),
            'creator': forms.HiddenInput(),
            'origin': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'class': 'form-control content-editor'}),
            'driving_question': forms.Textarea(attrs={'class': 'form-control content-editor'}),
            'publisher': forms.HiddenInput(),
            'publish_date': forms.HiddenInput(),  # forms.DateInput(attrs={'size': '40', 'type': 'date', 'placeholder': 'MM/DD/YYY'}),
            'contributors': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'icon': '(optional)',
            'active': 'Publish?',
            'description': 'Describe an overview of your project.',
            'contributors': 'List names of other collaborators separated by a comma. (optional)'
        }


class ProjectPrototypeCreateForm(ProjectPrototypeForm):

    def save(self):
        super(ProjectPrototypeCreateForm, self).save()
        
        if self.instance.active:
            self.instance.publish_date = datetime.now().date()
        else:
            self.instance.publish_date = None


        """ Create metadata objects from form data skipping fields listed in self.Meta.fields (base fields) """
        for i, j in self.cleaned_data.items():
            if i not in self.Meta.fields and j:
                if type(j) == list:
                    for k in j:
                        pm = PrototypeMetaElement(
                            prototype_project=self.instance, element_type=i, element_data=k)
                        pm.save()
                else:
                    pm = PrototypeMetaElement(
                        prototype_project=self.instance, element_type=i, element_data=j)
                    pm.save()
        return self.instance


class ProjectPrototypeUpdateForm(ProjectPrototypeForm):

    def save(self):        
        if 'active' in self.changed_data:
            if self.cleaned_data['active']:
                self.instance.publish_date = datetime.now().date()
            else:
                self.instance.publish_date = None 

        # if self.changed_data: self.instance.modified = datetime.now()
        super(ProjectPrototypeUpdateForm, self).save()

        prev_metadata = self.instance.data.all()

        """ Clear all previously assigned metadata objects """
        for i in prev_metadata:
            i.delete()
   
        """ Reassign metadata objects from form data skipping fields listed in self.Meta.fields (base fields) """
        for i, j in self.cleaned_data.items():

            if i not in self.Meta.fields and j:
                if type(j) == list:
                    for k in j:
                        pm = PrototypeMetaElement(
                            prototype_project=self.instance, element_type=i, element_data=k)
                        pm.save()
                else:
                    pm = PrototypeMetaElement(
                        prototype_project=self.instance, element_type=i, element_data=j)
                    pm.save()

        return self.instance


class TaskCreateForm(forms.ModelForm):

    class Meta:
        model = ProjectTask
        fields = ('title', 'prototype_project', 'short_description', 'description', 'task_category', 'sequence_order', 'task_type', 'task_focus', 'task_time', 'technology_tips',
                  'task_extension', 'potential_hurdles')
        labels = {'title': 'Task Title'}
        widgets = {
            'prototype_project': forms.HiddenInput(),
            'short_description': forms.Textarea(attrs={'rows': '2'}),
            'description': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'technology_tips': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'task_extension': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'potential_hurdles': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'task_category': forms.RadioSelect(),
            'task_type': forms.RadioSelect(),
            'task_focus': forms.RadioSelect(),
        }


class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model = ProjectTask
        fields = ('title', 'prototype_project', 'short_description', 'description', 'task_category', 'sequence_order', 'task_type', 'task_focus', 'task_time', 'technology_tips',
                  'task_extension', 'potential_hurdles')
        labels = {'title': 'Task Title'}
        widgets = {
            'prototype_project': forms.HiddenInput(),
            'short_description': forms.Textarea(attrs={'rows': '2'}),
            'description': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'technology_tips': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'task_extension': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'potential_hurdles': forms.Textarea(attrs={'class': 'form-control content-editor', 'rows': '3'}),
            'task_category': forms.RadioSelect(),
            'task_type': forms.RadioSelect(),
            'task_focus': forms.RadioSelect(),
        }


class ImplementationInfoCreateForm(forms.ModelForm):

    class Meta:
        model = ProjectImplementationInfo
        fields = ('title', 'prototype_project', 'description', 'sequence_order',)
        labels = {'title': 'Implementation Info Item Title'}
        widgets = {
            'prototype_project': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'class': 'form-control content-editor'}),
        }


class FileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(FileUploadForm, self).__init__(*args, **kwargs)
        # self.Meta.fields['project'].choices = self.request.user.projects.all()

    class Meta:
        model = ProjectFile
        fields = ('file', 'project', 'user')
        widgets = {'user': forms.HiddenInput(), 'project': forms.HiddenInput(), 'file': ClearableFileInput()}


class TaskFileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(TaskFileUploadForm, self).__init__(*args, **kwargs)
        # self.Meta.fields['project'].choices = self.request.user.projects.all()

    class Meta:
        model = TaskFile
        fields = ('file', 'task', 'user')
        widgets = {'user': forms.HiddenInput(), 'task': forms.HiddenInput(),'file': ClearableFileInput()}


class ImplementationFileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(ImplementationFileUploadForm, self).__init__(*args, **kwargs)
        # self.Meta.fields['project'].choices = self.request.user.projects.all()

    class Meta:
        model = ImplementationFile
        fields = ('file', 'implementation', 'user')
        widgets = {'user': forms.HiddenInput(), 'implementation': forms.HiddenInput(),'file': ClearableFileInput()}

