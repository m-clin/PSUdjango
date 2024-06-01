from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, Student, OrgMember, College, Program
from studentorg.forms import OrganizationForm, StudentForm, OrgMemberForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count, OuterRef, Subquery
from django.db.models.functions import TruncYear


@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass


class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'organizations.html'
    paginate_by = 8
    
    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
        return qs

    
class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization_add.html'
    success_url = reverse_lazy('organization-list')


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization_edit.html'
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'organization_delete.html'
    success_url = reverse_lazy('organization-list')


class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'students.html'
    paginate_by = 8
    
    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(lastname__icontains=query) | Q(firstname__icontains=query) |
                           Q(student_id__icontains=query) | Q(middlename__icontains=query))
        
        return qs


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_delete.html'
    success_url = reverse_lazy('student-list')


class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmembers.html'
    paginate_by = 8
    
    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student__lastname__icontains=query) | Q(student__firstname__icontains=query) |
                           Q(organization__name__icontains=query) | Q(date_joined__icontains=query))
        
        return qs


class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')


class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')


class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_delete.html'
    success_url = reverse_lazy('orgmember-list')


class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'colleges.html'
    paginate_by = 80

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query))
        
        return qs


class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')


class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')


class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_delete.html'
    success_url = reverse_lazy('college-list')


class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'programs.html'
    paginate_by = 8
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) | Q(college__name__icontains=query))
        
        return qs


class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')


class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_delete.html'
    success_url = reverse_lazy('program-list')

    
def student_count_by_program(request):
    data = Program.objects.annotate(student_count=Count('student')).values('prog_name', 'student_count')
    return JsonResponse(list(data), safe=False)


def student_distribution_by_organization(request):
    data = Organization.objects.annotate(student_count=Count('orgmember__student')).values('name', 'student_count')
    return JsonResponse(list(data), safe=False)


def get_org_members_per_year(request):
    # Get the members of all organizations grouped by the year they joined
    members_per_year = OrgMember.objects.annotate(year=TruncYear('date_joined')) \
                                 .values('year') \
                                 .annotate(count=Count('id')) \
                                 .order_by('year') \
                                 .values('year', 'count')

    data = list(members_per_year)
    return JsonResponse(data, safe=False)


def organizations_per_college(request):
    colleges = College.objects.annotate(
        org_count=Count('organization'),
    ).values('name', 'org_count')

    data = list(colleges)
    return JsonResponse(data, safe=False)


def student_count_by_college(request):
    data = College.objects.annotate(student_count=Count('program__student')).values('name', 'student_count')
    return JsonResponse(list(data), safe=False)


def students_without_organizations_per_year(request):
    # Get the list of student ids that are in the OrgMember table
    org_member_subquery = OrgMember.objects.filter(student_id=OuterRef('pk')).values('student_id')
    
    # Get the students who are not in the OrgMember table
    students = Student.objects.annotate(
        has_org=Subquery(org_member_subquery)
    ).filter(has_org__isnull=True)

    # Annotate students by the year they enrolled
    students_per_year = students.annotate(year=TruncYear('created_at')).values('year').annotate(count=Count('id')).order_by('year')

    data = list(students_per_year)
    return JsonResponse(data, safe=False)