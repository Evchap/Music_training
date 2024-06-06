from django.urls import path
from . import views

urlpatterns = [ # page 353
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-course/', # page 356
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'),

]
