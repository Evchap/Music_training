from django.shortcuts import render

from django.shortcuts import render

from .models import Subject


def index(request):

    all_courses = Subject.objects.all() # objects - менеджер
    print("all_courses", all_courses)
    return render(request, "courses/index.html")


from django.views.generic.list import ListView # page 321
from .models import Course

# class ManageCourseListView(ListView): # page 321 # обработчик для создания, редактирования и удаления курсов
#     model = Course
#     template_name = 'courses/manage/course/list.html'
#     def get_queryset(self):
#         qs = super(ManageCourseListView, self).get_queryset()
#         return qs.filter(owner=self.request.user)


from django.urls import reverse_lazy # page 321
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course

class OwnerMixin(object): # page 321 обработчик для подучения базового QuerySetʼа, с которым будет работать обработчик. М
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object): # page 321
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin): # page 321
    model = Course

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin): # page 321
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView): # page 321
    template_name = 'courses/manage/course/list.html'

class CourseCreateView(OwnerCourseEditMixin, CreateView): # page 321
    pass

class CourseUpdateView(OwnerCourseEditMixin, UpdateView): # page 321
    pass

class CourseDeleteView(OwnerCourseMixin, DeleteView): # page 321
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
