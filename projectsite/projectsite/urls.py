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
from django.urls import path, re_path
from studentorg import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.HomePageView.as_view(), name='home'),
    path('organization_list', v.OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', v.OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', v.OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', v.OrganizationDeleteView.as_view(), name='organization-delete'),
    
    path('student_list', v.StudentList.as_view(), name='student-list'),
    path('student_list/add', v.StudentCreateView.as_view(), name='student-add'),
    path('student_list/<pk>', v.StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<pk>/delete', v.StudentDeleteView.as_view(), name='student-delete'),
    
    path('orgmember_list', v.OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmember_list/add', v.OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/<pk>', v.OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/<pk>/delete', v.OrgMemberDeleteView.as_view(), name='orgmember-delete'),
    
    path('college_list', v.CollegeList.as_view(), name='college-list'),
    path('college_list/add', v.CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<pk>', v.CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/<pk>/delete', v.CollegeDeleteView.as_view(), name='college-delete'),
    
    path('program_list', v.ProgramList.as_view(), name='program-list'),
    path('program_list/add', v.ProgramCreateView.as_view(), name='program-add'),
    path('program_list/<pk>', v.ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/<pk>/delete', v.ProgramDeleteView.as_view(), name='program-delete'),
    
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

]