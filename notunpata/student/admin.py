from django.contrib import admin
from .models import School, Student, ExamDetails, Marks

# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ("id", "name")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ("roll_number", "name", "father_name", "mobile_no", "school", "student_class")

@admin.register(ExamDetails)
class ExamDetailsAdmin(admin.ModelAdmin):
	list_display = ("venue", "exam_date", "start_time", "end_time")
@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
	list_display = ("student", "marks")