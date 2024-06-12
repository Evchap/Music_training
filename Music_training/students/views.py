from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


class StudentRegistrationView(CreateView): # page 352 Обработка регистрации обучающихся в системе
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form): # page 352
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                             password=cd['password1'])
        login(self.request, user)
        return result


from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm

class StudentEnrollCourseView(LoginRequiredMixin, FormView): # page 355 обработчик
                                    #занимается зачислением студентов на курсы.
    template_name = 'courses/course/detail.html'  # page 356
    course = None
    form_class = CourseEnrollForm # форма которая при успешной валидации будет создавать
                                    # связь между студентом и курсом.
    def form_valid(self, form): # page 355
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self): # page 355 возвращает  адрес,  на  который  пользователь
                                # будет перенаправлен  после  успешной  обработки  формы.
        return reverse_lazy('student_course_detail', args=[self.course.id])


from django.views.generic.list import ListView
from courses.models import Course

class StudentCourseListView(LoginRequiredMixin, ListView): # page 357
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self): # page 357
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


from django.views.generic.detail import DetailView

class StudentCourseDetailView(DetailView): # page 357
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self): # page 358
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs): # page 358
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        # Получаем объект курса.
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # Получаем текущий модуль по параметрам запроса.
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # Получаем первый модуль.
            context['module'] = course.modules.all()[0]
        return context
