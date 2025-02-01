from django import forms
from .models import Student, School
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
	school_name = forms.ModelChoiceField(queryset=School.objects.all(), label="School")
	student_class = forms.ChoiceField(choices=[(i, f"Class {i}") for i in range(5, 13)], label="Class")

	class Meta:
		model = Student
		fields = ['name', 'father_name', 'mobile_no', 'student_class', 'school_name']

	def save(self, commit=True):
		school_name = self.cleaned_data.pop('school_name')
		school, created = School.objects.get_or_create(name=school_name)
		self.instance.school = school
		return super().save(commit)

class ConfirmStudentForm(forms.Form):
	name = forms.CharField(max_length=255, widget=forms.HiddenInput())
	father_name = forms.CharField(max_length=255, widget=forms.HiddenInput())
	mobile_no = forms.CharField(max_length=15, widget=forms.HiddenInput())
	student_class = forms.IntegerField(widget = forms.HiddenInput())
	school_name = forms.CharField(max_length=255, widget=forms.HiddenInput())
	roll_number = forms.CharField(max_length=10, widget=forms.HiddenInput())

# Form for adding marks to a student
class AddMarksForm(forms.Form):
    roll_number = forms.CharField(max_length=8, label="Roll Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    marks = forms.FloatField(label="Marks", widget=forms.NumberInput(attrs={'class': 'form-control'}))

# Form for deleting a school
class DeleteSchoolForm(forms.Form):
    confirm = forms.BooleanField(label="Are you sure you want to delete this school and all associated students?", required=True)