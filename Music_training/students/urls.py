from django.urls import path
from . import views

urlpatterns = [ # page 353
    path('register/', # page 353
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-course/', # page 356
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'),
    path('courses/', # page 358
        views.StudentCourseListView.as_view(),
        name='student_course_list'),
    path('course/<pk>/',  # page 358
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail'),
    path('course/<pk>/<module_id>/', # page 358
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail_module'),

]
