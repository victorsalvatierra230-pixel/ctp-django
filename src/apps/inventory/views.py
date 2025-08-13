from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View, generic
from apps.inventory.models import Assignment, Computer, Course, Matter, Person
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone

# Create your views here.

class ComputerCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Computer
    fields = '__all__'
    template_name = 'computer/create.html'
    success_url = reverse_lazy('inventory:list-computer')

    def get_success_url(self):
        messages.success(self.request, "¡¡Se ha creado con éxito!!")
        return super().get_success_url()

    def form_valid(self, form):
        try:
            print("Intentando guardar la computadora:", form.cleaned_data)
            return super().form_valid(form)
        except IntegrityError as e:
            print("Error de integridad:", e)
            messages.error(self.request, "Ya existe una computadora con este número.")
            form.add_error('number', "Este número ya está en uso.")
            return self.form_invalid(form)

    
class ComputerListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Computer
    template_name = 'computer/list.html'
    context_object_name = 'computers'
    paginate_by = 10
    
    def get_queryset(self):
        return Computer.objects.filter(is_deleted=False).order_by('number')
       
class ComputerDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        computer = get_object_or_404(Computer, pk=pk)
        computer.is_deleted = True
        computer.save()
        messages.success(request, "¡¡Se ha eliminado con éxito!!")
        return redirect('inventory:list-computer')

class ComputerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Computer
    fields = '__all__'
    template_name = 'computer/update.html'
    success_url = reverse_lazy('inventory:list-computer')
    context_object_name = 'computers'

    
    def get_success_url(self) -> str:
        messages.success(self.request, "¡¡Se ha actualizado con éxito!!")
        return super().get_success_url()

class PersonCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Person
    fields = '__all__'
    template_name = 'person/create.html'
    success_url = reverse_lazy('inventory:list-person')
    
    def get_success_url(self) -> str:
        messages.success(self.request, "¡¡Se ha creado con éxito!!")
        return super().get_success_url()
    
class PersonListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Person
    template_name = 'person/list.html'
    context_object_name = 'persons'
    paginate_by = 10
    
    def get_queryset(self):
        return Person.objects.filter(is_deleted=False)
    
class PersonDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def post(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        person.is_deleted = True
        person.save()
        messages.success(request, "¡¡Se ha eliminado con éxito!!")
        return redirect('inventory:list-person')


class PersonUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Person
    fields = '__all__'
    template_name = 'person/update.html'
    success_url = reverse_lazy('inventory:list-person')
    context_object_name = 'persons'

    def get_success_url(self) -> str:
        messages.success(self.request, "¡¡Se ha actualizado con éxito!!")
        return super().get_success_url() 


class MatterListFilterView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Matter
    template_name = 'matter/list.html'
    context_object_name = 'matters'
   
    def get_queryset(self):
        queryset = Matter.objects.filter(is_deleted=False)
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(Q(course__first_name__icontains=search)).distinct()
        return queryset
    
class AssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Assignment
    fields = ['computer']  # el resto los capturas por POST directamente o con campos ocultos
    template_name = 'assignment/create.html'
    success_url = reverse_lazy('inventory:list-assignment')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['computers'] = Computer.objects.filter(
            is_available=True,
            is_technical_issue=False
        )
        context['courses'] = Course.objects.filter(is_deleted=False)

        course_id = self.request.GET.get('course_id')
        if course_id:
            context['matters'] = Matter.objects.filter(course_id=course_id, is_deleted=False)
            context['selected_course'] = int(course_id)
        else:
            context['matters'] = Matter.objects.none()
            context['selected_course'] = None
        return context

    def form_valid(self, form):
        course_id = self.request.POST.get('course')
        matter_id = self.request.POST.get('matter')
        dni = self.request.POST.get('dni')

        if not course_id or not matter_id:
            messages.error(self.request, "Debe seleccionar curso y materia.")
            return self.form_invalid(form)

        try:
            person = Person.objects.get(dni=dni)
        except Person.DoesNotExist:
            messages.error(self.request,"No se encontró ninguna persona con este DNI.")
            return self.form_invalid(form)

        # Validar si ya tiene asignación
        if Assignment.objects.filter(person=person, returned=False).exists():
            messages.error(self.request, "Ya tenes una computadora asignada.")
            return self.form_invalid(form)

        computer = form.cleaned_data['computer']
        if not computer.is_available or computer.is_technical_issue:
            form.add_error('computer', 'La computadora seleccionada no está disponible.')
            return self.form_invalid(form)
        computer = form.cleaned_data['computer']

        

        assignment = form.save(commit=False)
        assignment.person = person
        assignment.course_id = course_id  

        assignment.save()

        computer.is_available = False
        computer.save()

        messages.success(self.request, "¡Se ha reservado con éxito!")
        return super().form_valid(form)

class AssignmentStudentCreateView(generic.CreateView):
    model = Assignment
    fields = ['computer'] 
    template_name = 'assignment/register_student.html'
    success_url = reverse_lazy('inventory:create-assignment-student')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['computers'] = Computer.objects.filter(is_available=True)
        context['courses'] = Course.objects.filter(is_deleted=False)

        course_id = self.request.GET.get('course_id')
        if course_id:
            context['matters'] = Matter.objects.filter(course_id=course_id, is_deleted=False)
            context['selected_course'] = int(course_id)
        else:
            context['matters'] = Matter.objects.none()
            context['selected_course'] = None
        return context

    def form_valid(self, form):
        course_id = self.request.POST.get('course')
        matter_id = self.request.POST.get('matter')
        dni = self.request.POST.get('dni')

        if not course_id or not matter_id:
            messages.error(self.request, "Debe seleccionar curso y materia.")
            return self.form_invalid(form)

        try:
            person = Person.objects.get(dni=dni)
        except Person.DoesNotExist:
            messages.error(self.request,"No se encontró ninguna persona con este DNI.")
            return self.form_invalid(form)

        # Validar si ya tiene asignación
        if Assignment.objects.filter(person=person, returned=False).exists():
            messages.error(self.request, "Ya tenes una computadora asignada.")
            return self.form_invalid(form)

        computer = form.cleaned_data['computer']
        if not computer.is_available:
            form.add_error('computer', 'La computadora seleccionada no está disponible.')
            return self.form_invalid(form)

        assignment = form.save(commit=False)
        assignment.person = person
        assignment.course_id = course_id 

        assignment.save()

        computer.is_available = False
        computer.save()

        messages.success(self.request, "¡Se ha reservado con éxito!")
        return super().form_valid(form)


        
class AssignmentListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Assignment
    template_name = 'assignment/list.html'
    context_object_name = 'assignments'
    paginate_by = 10 
    
    def get_queryset(self):
        return Assignment.objects.filter(is_deleted=False)

class AssignmentUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Assignment
    fields = ('observation',)
    template_name = 'assignment/update.html'
    context_object_name = 'assignments'
    success_url = reverse_lazy('inventory:list-assignment')

    def get_success_url(self) -> str:
        messages.success(self.request, "¡¡Se ha actualizado con éxito!!")
        return super().get_success_url()

class ToggleAvailabilityView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def post(self, request, pk):
        computer = get_object_or_404(Computer, pk=pk)

        # Cambiar disponibilidad
        computer.is_available = not computer.is_available
        computer.save()

        # Si se volvió disponible, marcamos el assignment como eliminado
        if computer.is_available:
            assignment = Assignment.objects.filter(computer=computer, returned=False, is_deleted=False).first()
            if assignment:
                assignment.is_deleted = True
                assignment.returned = True  # opcional, si querés marcarlo como devuelto también
                assignment.returned_at = timezone.now()
                assignment.save()

        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('inventory:list-computer')))

class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Course
    fields = '__all__'
    template_name = 'course/create.html'
    success_url = reverse_lazy('inventory:list-course')

    def get_success_url(self):
        messages.success(self.request, "¡¡Se ha creado con éxito!!")
        return super().get_success_url()

class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Course
    template_name = 'course/list.html'
    context_object_name = 'courses'
    paginate_by = 10
    
    def get_queryset(self):
        return Course.objects.filter(is_deleted=False)

class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Course
    fields = '__all__'
    template_name = 'course/update.html'
    context_object_name = 'courses'
    success_url = reverse_lazy('inventory:list-course')

    def get_success_url(self):
        messages.success(self.request, "¡¡Se ha actualizado con éxito!!")
        return super().get_success_url()


class MatterCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Matter
    fields = '__all__'
    template_name = 'matter/create.html'
    success_url = reverse_lazy('inventory:list-matter')

    def get_success_url(self):
        messages.success(self.request, "¡¡Se ha creado con éxito!!")
        return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(is_deleted=False)
        return context


class MatterListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Matter
    template_name = 'matter/list.html'
    context_object_name = 'matters'
    paginate_by = 10
    
    def get_queryset(self):
        return Matter.objects.filter(is_deleted=False)


class MatterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Matter
    fields = '__all__'
    template_name = 'matter/update.html'
    context_object_name = 'matter'
    success_url = reverse_lazy('inventory:list-matter')

    def get_success_url(self):
        messages.success(self.request, "¡Materia actualizada con éxito!")
        return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(is_deleted=False)
        return context
