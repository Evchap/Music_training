from django.urls import path
from . import views

urlpatterns = [ # page 353
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
]
