from django.urls import path
from apps.inventory.views import AssignmentListView, AssignmentStudentCreateView, AssignmentUpdateView, ComputerCreateView, CourseCreateView, CourseListView, CourseUpdateView, MatterCreateView, MatterListFilterView, MatterListView, MatterUpdateView, ToggleAvailabilityView
from apps.inventory.views import ComputerListView
from apps.inventory.views import ComputerDeleteView
from apps.inventory.views import ComputerUpdateView
from apps.inventory.views import AssignmentCreateView

from apps.inventory.views import PersonCreateView
from apps.inventory.views import PersonListView
from apps.inventory.views import PersonDeleteView
from apps.inventory.views import PersonUpdateView


app_name = 'inventory'

urlpatterns = [
    path('computer/create/', ComputerCreateView.as_view(), name='create-computer'),
    path('computer/list/', ComputerListView.as_view(), name='list-computer'),
    path('computer/delete/<int:pk>', ComputerDeleteView.as_view(), name='delete-computer'),
    path('computer/update/<int:pk>', ComputerUpdateView.as_view(), name='update-computer'),
    
    path('person/create/', PersonCreateView.as_view(), name='create-person'),
    path('person/list/', PersonListView.as_view(), name='list-person'),
    path('person/delete/<int:pk>', PersonDeleteView.as_view(), name='delete-person'),
    path('person/update/<int:pk>', PersonUpdateView.as_view(), name='update-person'),
    path('search/', MatterListFilterView.as_view(), name='filter-matter'),
    
    path('assignment/create/', AssignmentCreateView.as_view(), name='create-assignment'),
    path('assignment/list/', AssignmentListView.as_view(), name='list-assignment'),
    path('assignment/update/<int:pk>',  AssignmentUpdateView.as_view(), name='update-assignment'),
    path('computer/<int:pk>/toggle/', ToggleAvailabilityView.as_view(), name='toggle-availability'),
    path('assignment/student/create/', AssignmentStudentCreateView.as_view(), name='create-assignment-student'),

    path('course/create/', CourseCreateView.as_view(), name='create-course'),
    path('course/list/', CourseListView.as_view(), name='list-course'),
    path('course/update/<int:pk>',  CourseUpdateView.as_view(), name='update-course'),

    path('matter/create/', MatterCreateView.as_view(), name='create-matter'),
    path('matter/list/', MatterListView.as_view(), name='list-matter'),
    path('matter/update/<int:pk>',  MatterUpdateView.as_view(), name='update-matter'),
]


