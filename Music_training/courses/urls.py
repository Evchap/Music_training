from django.urls import path
from django.urls import path
from . import views
from .views import index



app_name = 'courses'
urlpatterns = [
    path('', index, name='index'),

    path('mine/', # page 326
          views.ManageCourseListView.as_view(),
          name='manage_course_list'),
    path('create/', # page 326
          views.CourseCreateView.as_view(),
          name='course_create'),
    path('<pk>/edit/', # page 326
          views.CourseUpdateView.as_view(),
          name='course_edit'),
    path('<pk>/delete/', # page 326
          views.CourseDeleteView.as_view(),
          name='course_delete'),
]
