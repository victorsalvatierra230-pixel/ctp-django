from django.db import models

class Computer(models.Model):
    number = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"PC #{self.number}"

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.PositiveIntegerField(unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
     
class Course(models.Model):
    first_name = models.CharField(max_length=100) 
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.first_name}" 

class Matter(models.Model):
    first_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="matters")
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} ({self.course.first_name})"
    
class Assignment(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    observation = models.CharField(max_length=255, default='Sin observaciones')
    returned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.person} - PC #{self.computer.number}"
