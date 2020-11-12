import string
import random
from collections import OrderedDict, namedtuple

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from model_utils.models import TimeStampedModel
from filebrowser.fields import FileBrowseField

from discussions.models import Post

from .schema import PrototypeMetadataForm, METADATA_CATEGORIES, METADATA_TYPES, METADATA_TYPES_TO_CATEGORIES


class ProjectPrototype(TimeStampedModel):
    title = models.CharField(max_length=512, unique=True)
    creator = models.ForeignKey(User, related_name='projects')
    origin = models.ForeignKey(
        'self', null=True, blank=True, related_name='flips')
    description = models.TextField()
    publisher = models.CharField(
        max_length=512, default='National Foreign Language Resource Center')
    publish_date = models.DateField(null=True, blank=True)
    contributors = models.TextField(null=True, blank=True)
    rights = models.CharField(max_length=512, null=True, blank=True)
    uri = models.CharField(max_length=512, null=True, blank=True)
    active = models.BooleanField(
        default=False, help_text="Hide/unhide this project")
    icon = models.FileField(
        upload_to='uploads', null=True, blank=True)
    featured = models.BooleanField(default=False)
    featured_by_line = models.TextField(null=True, blank=True)
    driving_question = models.TextField()

    def clone_project(self, user):
        rstr = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for x in range(4))
        new_title = self.title + '-' + user.last_name + '-' + rstr

        try:
            # Copy object attributes
            clone = ProjectPrototype(
                title=new_title, creator=user, origin=self, description=self.description, publisher=self.publisher, rights=self.rights)
            clone.save()

            # Copy object metadata
            for i in self.data.all():
                pm = PrototypeMetaElement(
                    prototype_project=clone, element_type=i.element_type, element_data=i.element_data)
                pm.save()

            # Copy object tasks
            for i in self.tasks.all():
                new_t = i.clone_task()
                new_t.prototype_project = clone
                new_t.save()

        except:
            pass

        return clone

    def meta_data_schema(self):
        return PrototypeMetadataForm()

    def get_element_data(self, element_type):
        data = [i.element_data for i in self.data.filter(
            element_type=element_type)]
        return data

    def get_languages(self):
        return self.get_element_data('language')

    def get_data_list(self):
        return {i.element_type: i.element_data for i in self.data.all().order_by('element_category')}
                   
    def get_data_dict(self):
        """ Group element data by element_type. Returns a dict keyed by element_type name. """

        """
        Using a namedtuple here to gather display string and data items.
        """
        MetaElement = namedtuple(
            'MetaElement', 'metaprefix displayname datalist')
        data_dict = OrderedDict()
        field_order = self.meta_data_schema().fields.items()

        for field_name, field_type in field_order:
            data_dict[field_name] = MetaElement(
                metaprefix=field_type.label,
                displayname=field_type.label_suffix,
                datalist=[]
            )

        for i in self.data.all().order_by('element_type'):
            try:
                data_dict[i.element_type].datalist.append(i.element_data)
            except:
                data_dict[i.element_type] = []
                data_dict[i.element_type].append(i.element_data)

        return data_dict

    def get_data(self):
        data_dict = {}
        for i in self.data.all().order_by('element_category'):
            try:
                data_dict[i.element_category].append((i.get_element_type_display, i.element_data))
            except:
                data_dict[i.element_category] = []
                data_dict[i.element_category].append((i.get_element_type_display, i.element_data))        
        return data_dict

    def save(self, *args, **kwargs):
        """ Create comment thread if one does not exist"""
        super(ProjectPrototype, self).save(*args, **kwargs)
        if not ProjectComment.objects.filter(project=self):
            thread = Post(text='Project Comments', creator=self.creator, subject='Comments for project')
            thread.save()
            ProjectComment(thread=thread, project=self).save()

    def get_absolute_url(self):
        return reverse('view_prototype', args=[self.id])

    def __unicode__(self):
        return self.title

    class Meta:
        pass


class PrototypeMetaElement(models.Model):
    prototype_project = models.ForeignKey(
        ProjectPrototype, related_name='data')
    element_type = models.CharField(max_length=512, choices=METADATA_TYPES)
    element_data = models.TextField()
    element_category = models.CharField(max_length=512, blank=True, null=True, choices=METADATA_CATEGORIES)

    def save(self, *args, **kwargs):
        super(PrototypeMetaElement, self).save(*args, **kwargs)
        try:
            self.element_category = METADATA_TYPES_TO_CATEGORIES[self.element_type]
            super(PrototypeMetaElement, self).save(*args, **kwargs)
        except:
            print ('Error while trying to assign a category to element. Refer to schema.py')

    class Meta:
        unique_together = (
            ('prototype_project', 'element_type', 'element_data'),)


TASK_CATEGORIES = (
    ('0_preparing', 'Preparing for the Project'),
    ('1_launching', 'Launching the Project'),
    ('2_managing', 'Managing the Project'),
    ('3_assessment', 'Assessment'),
)

TASK_TYPES = (
    ('driving question', 'Driving question'),
    ('need to know', 'Need to know'),
    ('scaffolding', 'Scaffolding')
)

TASK_FOCI = (
    ('content', 'Content'),
    ('grammar', 'Grammar'),
    ('interaction', 'Interaction'),
    ('technology', 'Technology'),
    ('feedback and/or revision', 'Feedback and/or revision'),
    ('reflection', 'Reflection'),
)


class ProjectTask(models.Model):
    title = models.CharField(max_length=512)
    short_description = models.TextField(
        default='A sentence that summarizes this task.')
    task_category = models.CharField(
        max_length=48, null=True, choices=TASK_CATEGORIES)
    task_type = models.CharField(max_length=48, blank=True, choices=TASK_TYPES)
    task_focus = models.CharField(max_length=48, blank=True, choices=TASK_FOCI)
    task_time = models.CharField(max_length=48, blank=True)
    description = models.TextField()
    technology_tips = models.TextField(blank=True)
    task_extension = models.TextField(blank=True)
    potential_hurdles = models.TextField(blank=True)
    prototype_project = models.ForeignKey(
        ProjectPrototype, null=False, related_name='tasks')
    sequence_order = models.IntegerField(default=0)

    def creator(self):
        return self.prototype_project.creator

    def clone_task(self):
        t1 = self
        t1.pk = None
        t1.save()
        return t1

    def get_absolute_url(self):
        return reverse('view_task', args=[self.prototype_project.id, self.id])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['task_category', 'sequence_order']


class ProjectComment(models.Model):
    thread = models.ForeignKey(Post, related_name='project_thread')
    project = models.ForeignKey(ProjectPrototype, related_name='project_discussion')

    class Meta:
        verbose_name = 'Project / Discussion Pair'

    def __unicode__(self):
        return '%s --> %s' % (self.project, self.thread)


class ProjectImplementationInfo(models.Model):
    """Component to allow users to attach general implementation information to project."""

    title = models.CharField(max_length=512)
    description = models.TextField()
    prototype_project = models.ForeignKey(
        ProjectPrototype, null=False, related_name='implementation_info')
    sequence_order = models.IntegerField(default=0)

    def creator(self):
        return self.prototype_project.creator

    def get_absolute_url(self):
        return reverse('view_implementation_item', args=[self.prototype_project.id, self.id])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sequence_order']


class ProjectCoeditors(models.Model):
    prototype_project = models.ForeignKey(
        ProjectPrototype, null=False, related_name='coeditors')
    coeditor = models.ForeignKey(User, related_name='coedited_projects')


class RepoPage(TimeStampedModel):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    thumbnail_desc = models.CharField(
        max_length=160, default='more...', null=True, blank=True, )
    image = models.CharField(max_length=100, blank=True, default='icon.png',
                             verbose_name='Icon image file name')
    listing_rank = models.IntegerField(blank=True, default=0, help_text='default rank. higher the number, lower the rank')
    featured = models.BooleanField(blank=True, default=False)
    featured_rank = models.IntegerField(blank=True, default=0, help_text='higher the number, lower the rank')
    headline = models.BooleanField(default=False)
    headline_tag = models.CharField(
        max_length=512, blank=True, null=True, default='')
    private = models.BooleanField(default=False, blank=True, help_text='checking this ON will require a user to login to view this story')

    def get_absolute_url(self):
        return reverse('page_view', args=[str(self.id)])

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'reposite' 


class ProjectFile(TimeStampedModel):
    file = models.FileField(
        upload_to='uploads')
    project = models.ForeignKey(ProjectPrototype, related_name='project_files')
    user = models.ForeignKey(User, related_name='uploaded_files')


class TaskFile(TimeStampedModel):
    file = models.FileField(upload_to='uploads')
    task = models.ForeignKey(ProjectTask, related_name='task_files')
    user = models.ForeignKey(User, related_name='uploaded_task_files')


class ImplementationFile(TimeStampedModel):
    file = models.FileField(
        upload_to='uploads')
    implementation = models.ForeignKey(ProjectImplementationInfo, related_name='implementation_files')
    user = models.ForeignKey(User, related_name='uploaded_implementation_files')
