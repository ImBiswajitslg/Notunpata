from django.db import models
from datetime import datetime

# Create your models here.
class School(models.Model):
	name = models.CharField(max_length=255, unique=True)
	def __str__(self):
		return self.name

class Student(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)  
	father_name = models.CharField(max_length=255, blank=True, null=True)  
	mobile_no = models.CharField(max_length=15, blank=True, null=True)  
	student_class = models.IntegerField(choices=[(i, f"Class {i}") for i in range(5,13)])  
	school = models.ForeignKey('School', on_delete=models.CASCADE)  # Nullable foreign key
	roll_number = models.CharField(max_length=10, unique=True, null=True)  # Optional and unique
	registration_year = models.IntegerField(blank=True, null=True)
	serial_number = models.PositiveIntegerField(null=True, blank=True)  

	def __str__(self):
		return f"{self.name} ({self.roll_number})"

class ExamDetails(models.Model):
	venue = models.CharField(max_length=255)
	exam_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()

	def __str__(self):
		return self.venue
class Marks(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	marks = models.FloatField()

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['student'], name='unique_student_marks')
		]

	def __str__(self):
		return f"{self.student.name} - {self.marks}"