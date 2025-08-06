from django.contrib import admin
from .models import Computer, Person, Assignment, Matter, Course

# Admin para Computer
@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('number', 'first_name', 'description', 'is_available', 'is_deleted')
    list_filter = ('is_available', 'is_deleted')
    search_fields = ('number', 'first_name', 'description')
    ordering = ('number',)
    list_editable = ('is_available',)


# Admin para Assignment
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('person', 'computer', 'course', 'requested_at', 'returned', 'returned_at', 'is_deleted')
    list_filter = ('returned', 'is_deleted', 'requested_at')
    search_fields = ('person__first_name', 'person__last_name', 'computer__first_name', 'course__first_name')
    ordering = ('-requested_at',)
    date_hierarchy = 'requested_at'
    readonly_fields = ('requested_at', 'returned_at')


# Admin para Person
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('dni', 'last_name', 'first_name', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('dni', 'last_name', 'first_name')
    ordering = ('last_name',)


# Admin para Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('first_name',)
    ordering = ('first_name',)


# Admin para Matter
@admin.register(Matter)
class MatterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'course', 'is_deleted')
    list_filter = ('is_deleted', 'course')
    search_fields = ('first_name', 'course__first_name')
    ordering = ('first_name',)
    
