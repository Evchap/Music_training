from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View


class LogoutView(View): # нашел что-то похожее
    def get(self, request):
        logout(request)
        return redirect('login')


from django.views.generic.list import ListView
from .models import Course

# class ManageCourseListView(ListView): # page 321
#     model = Course
#     template_name = 'courses/manage/course/list.html'
#
#     def get_queryset(self): # page 321
#         qs = super(ManageCourseListView, self).get_queryset()
#         return qs.filter(owner=self.request.user)

from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course


class OwnerMixin(object): # page 322
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object): # page 322
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin): # page 322
    model = Course # page 322
    fields = ['subject', 'title', 'slug', 'overview'] # 325
    success_url = reverse_lazy('manage_course_list') # 325

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin): # page 322
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView): # page 322
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self): # page 321
        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)

# class CourseCreateView(OwnerCourseEditMixin, CreateView): # page 322
#     pass
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class CourseCreateView(  # 325
    PermissionRequiredMixin,
    OwnerCourseEditMixin,
    CreateView):
    permission_required = 'courses.add_course'

# class CourseUpdateView(OwnerCourseEditMixin, UpdateView): # page 322
#     pass

class CourseUpdateView(PermissionRequiredMixin,  # 325
                       OwnerCourseEditMixin,
                       UpdateView):
    permission_required = 'courses.change_course'

# class CourseDeleteView(OwnerCourseMixin, DeleteView): # page 322
#     template_name = 'courses/manage/course/delete.html' # page 322
#     success_url = reverse_lazy('manage_course_list')
class CourseDeleteView(PermissionRequiredMixin,  # 325
                       OwnerCourseMixin,
                       DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'

from django.shortcuts import redirect, get_object_or_404 # page 331
from django.views.generic.base import TemplateResponseMixin, View # page 331

from .forms import ModuleFormSet

class CourseModuleUpdateView(TemplateResponseMixin, View): # page 332
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None): # page 332
        return ModuleFormSet(instance=self.course,
        data=data)

    def dispatch(self, request, pk): # page 332
        self.course = get_object_or_404(Course,
                                         id=pk,
                                         owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs): # page 332
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs): # page 332
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                         'formset': formset})


from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content


class ContentCreateUpdateView(TemplateResponseMixin, View):  # 335
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):  # 335
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):  # 335
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)


    def get(self, request, module_id, model_name, id=None): # page 336
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None): # page 336
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # Создаем новый объект.
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})

class ContentDeleteView(View): # 338
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View): # page 339
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id): # page 339
        module = get_object_or_404(Module,
                                    id=module_id,
                                    course__owner=request.user)
        return self.render_to_response({'module': module})


from braces.views import CsrfExemptMixin, JsonRequestResponseMixin # 343

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View): # 343
    def post(self, request): # page 343
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                    course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View): # 343
    def post(self, request): # page 343
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


from django.db.models import Count
from .models import Subject


class CourseListView(TemplateResponseMixin, View):  # page 347
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):  # page 347
        subjects = Subject.objects.annotate(
        total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                    'subject': subject,
                                    'courses': courses})

from django.views.generic.detail import DetailView

class CourseDetailView(DetailView): # page 348 обработчик, который будет
                                    # показывать страницу курса
    model = Course
    template_name = 'courses/course/detail.html'




