from django.shortcuts import render

from django.shortcuts import render

from .models import Subject


def index(request):

    all_courses = Subject.objects.all() # objects - менеджер
    print("all_courses", all_courses)
    return render(request, "courses/index.html")


from django.views.generic.list import ListView # page 321
from .models import Course

class ManageCourseListView(ListView): # page 321 # обработчик запросов для создания, редактирования и удаления курсов
    model = Course
    template_name = 'courses/manage/course/list.html'
    def get_queryset(self):
        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)


from django.urls import reverse_lazy # page 321
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course

class OwnerMixin(object): # page 322 обработчик для подучения базового QuerySetʼа, с которым будет работать обработчик. М
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object): # page 322
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin): # page 322
    model = Course

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin): # page 322
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

# class ManageCourseListView(OwnerCourseMixin, ListView): # page 322
#     template_name = 'courses/manage/course/list.html'
#
# class CourseCreateView(OwnerCourseEditMixin, CreateView): # page 322
#     pass
#
# class CourseUpdateView(OwnerCourseEditMixin, UpdateView): # page 322
#     pass
#
# class CourseDeleteView(OwnerCourseMixin, DeleteView): # page 322
#     template_name = 'courses/manage/course/delete.html'
#     success_url = reverse_lazy('manage_course_list')

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # page 325 ограничение доступа к классам обработчикам.import


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin): # page 325
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class CourseCreateView(  # 325
    PermissionRequiredMixin,
    OwnerCourseEditMixin,
    CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, # 325
                       OwnerCourseEditMixin,
                       UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, # 325
                       OwnerCourseMixin,
                       DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'


from django.shortcuts import redirect, get_object_or_404 # page 332
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet

class CourseModuleUpdateView(TemplateResponseMixin, View): # page 332
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
        data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                         id=pk,
                                         owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                         'formset': formset})


