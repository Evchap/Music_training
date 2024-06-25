from django.urls import path
from . import views

apps_name = "courses"
urlpatterns = [
    path('mine/', # 326
          views.ManageCourseListView.as_view(),
          name='manage_course_list'),
    path('create/', # 326
          views.CourseCreateView.as_view(),
          name='course_create'),
    path('<pk>/edit/', # 326
          views.CourseUpdateView.as_view(),
          name='course_edit'),
    path('<pk>/delete/', # 326
          views.CourseDeleteView.as_view(),
          name='course_delete'),
    path('<pk>/module/', # page 333
        views.CourseModuleUpdateView.as_view(),
        name='course_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/',  # page 336
          views.ContentCreateUpdateView.as_view(),
          name='module_content_create'),

    path('module/<int:module_id>/content/<model_name>/<id>/', # page 336
          views.ContentCreateUpdateView.as_view(),
          name='module_content_update'),

    path('content/<int:id>/delete/', # page 339
          views.ContentDeleteView.as_view(),
          name='module_content_delete'),
    path('module/<int:module_id>/', # page 339
         views.ModuleContentListView.as_view(),
         name='module_content_list'),
    path('module/order/', # page 343
          views.ModuleOrderView.as_view(),
            name='module_order'),
    path('content/order/', # page 344
          views.ContentOrderView.as_view(),
          name='content_order'),
    path('subject/<slug:subject>)/', # page 349
          views.CourseListView.as_view(),
          name='course_list_subject'),
    path('<slug:slug>/', # page 349
          views.CourseDetailView.as_view(),
          name='course_detail'),

]
