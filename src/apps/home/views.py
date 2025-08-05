from typing import Any
from django import http
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.inventory.models import Assignment, Computer, Course, Matter, Person
# Create your views here.

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'home/index.html' 
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            computers = Computer.objects.filter(is_deleted=False)
            total_computers = computers.count()
            context['total_computers'] = total_computers
            
            assignments = Assignment.objects.filter(is_deleted=False)
            total_assignments = assignments.count()
            context['total_assignments'] = total_assignments
            
            person = Person.objects.filter(is_deleted=False)
            total_person = person.count()
            context['total_persons'] = total_person
        
            course = Course.objects.filter(is_deleted=False)
            total_course = course.count()
            context['total_courses'] = total_course
            
        
            matter = Matter.objects.filter(is_deleted=False)
            total_matter = matter.count()
            context['total_matters'] = total_matter
            return context


 