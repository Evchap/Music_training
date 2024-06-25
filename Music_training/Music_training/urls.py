"""
URL configuration for Music_training project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import index
from django.urls import path, include
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.conf.urls.static import static


import Music_training
# from Music_training.courses.views import CourseListView
# from courses.views import CourseListView
from courses.views import *
# from ..courses.views import CourseListView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # page 318 обработчик  входа подсистемы аутентификации
    path('accounts/logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post', 'options']),
         name='logout'),  # page 318 обработчик  выхода подсистемы аутентификации
    path('admin/', admin.site.urls),  # page 318
    path('course/', include('courses.urls')),  # 326
    path('', CourseListView.as_view(), name='course_list'), # page 348
    path('students/', include('students.urls')), # page 353
]

if settings.DEBUG: # page 361
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # page 361

