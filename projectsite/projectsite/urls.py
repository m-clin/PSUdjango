"""
URL configuration for projectsite project.

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
from django.contrib import admin
from django.urls import path
from studentorg import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.HomePageView.as_view(), name='home'),
    path('organization_list', v.OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', v.OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', v.OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', v.OrganizationDeleteView.as_view(), name='organization-delete'),
    path('student_list', v.StudentList.as_view(), name='student-list'),
    path('student_list/add', v.StudentCreateView.as_view(), name='student-add'),
]