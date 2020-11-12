# mixins.py


class ListUserFilesMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ListUserFilesMixin, self).get_context_data(**kwargs)
        if self.request.user:        	
        	file_tree = {}
        	file_tree['project'] = self.request.user.uploaded_files.all()
        	file_tree['task'] = self.request.user.uploaded_task_files.all().order_by('task')
        	file_tree['implementation'] = self.request.user.uploaded_implementation_files.all().order_by('implementation')
        	context['filelisting'] = file_tree
        return context
