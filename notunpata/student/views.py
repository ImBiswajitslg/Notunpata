from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, School, ExamDetails, Marks
from reportlab.pdfgen import canvas
from io import BytesIO
from .forms import StudentForm, ConfirmStudentForm
from datetime import datetime

@login_required
def add_student(request):
    if request.method == "POST":
    	form = StudentForm(request.POST)
    	if form.is_valid():
    		school = form.cleaned_data['school_name']
    		student_class = form.cleaned_data['student_class']
    		#Fetch the school instance
    		#school = School.objects.get(id=school_id)
    		#Calculate the serial number for this class in this school
    		current_year = datetime.now().year % 100 #get the last two digits of the year
    		max_roll = Student.objects.filter(
    			school = school,
    			student_class = student_class,
    			registration_year = current_year
    		).aggregate(Max('serial_number'))['serial_number__max'] or 0
    		new_serial = max_roll + 1

    		# Generate roll number
    		roll_number = f"{current_year:02}{school.id:02}{int(student_class):02}{new_serial:02}"

    		# Save the student with the generated roll number
    		student = form.save(commit=False)
    		student.school = school
    		student.registration_year = datetime.now().year
    		student.serial_number = new_serial
    		student.roll_number = roll_number
    		student.save()

    		return redirect("student:add_student")
    else:
    	form = StudentForm()
    schools = School.objects.all()
    return render(request, "student/add_student.html", {'form': form, 'schools' : schools})

def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			login(request, form.save())
			return redirect("student:login")
	else:
		form = UserCreationForm()
	return render(request, "student/register.html", {"form" : form})

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			#next_url = request.POST.get('next', 'student:admin_panel')
			if user.is_superuser:
				return redirect("student:admin_panel")
			else:
				return redirect("student:student")
	else:
		form = AuthenticationForm()
	next_url = request.GET.get('next', '')
	return render(request, "student/login.html", {'form':form, 'next': next_url})

def logout_view(request):
	logout(request)
	return redirect("student:login")

def admin_required(user):
	return user.is_superuser

@user_passes_test(admin_required)
def delete_school(request, school_id):
	school = get_object_or_404(School, id=school_id)
	if request.method == 'POST':
		school.delete() #Autometically deletes related students
		return redirect('admin_panel')
	return render(request, 'student/confirm_delete_school.html', {'school' : school})

@user_passes_test(admin_required)
def admin_panel(request):
	schools = School.objects.all()
	return render(request, 'student/admin_panel.html', {'schools' : schools})

@user_passes_test(admin_required)
def add_marks(request):
	if request.method == "POST":
		roll_number = request.POST.get('roll_number')
		marks = request.POST.get('marks')
		student = Student.objects.filter(roll_number=roll_number).first()

		if student:
			student.marks = marks #Assume 'marks' is a new field in student model
			student.save()
			return render(request, 'student/marks_added_html', {'student':student, 'marks':marks})
		else:
			return render(request, 'student/add_marks.html', {'error' : 'Student not found'})
	return render(request, 'student/add_marks.html')

@user_passes_test(admin_required)
def student_list(request):
	students = Student.objects.all()
	return render(request, 'student_list.html', {'students':stude})

def student(request):
	return render(request, 'student/student.html')

@login_required
def generate_admit_card(request):
	if request.user.is_superuser:
		#admin
		if request.method=="POST":
			venue = request.POST['venue']
			exam_date = request.POST['exam_date']
			start_time = request.POST['start_time']
			end_time = request.POST['end_time']
			# Create a buffer for the pdf
			buffer = BytesIO()
			p = canvas.Canvas(buffer)

			y_position = 800
			for student in Student.objects.all():
				if y_position < 100 :
					p,showPage()
					y_position = 800
				
				p.drawString(100, y_position, f"Name: {student.name}")
				p.drawString(100, y_position-20, f"Roll Number:{student.roll_number}")
				p.drawString(100, y_position-40, f"Venue: {venue}")
				p.drawString(100, y_position-60, f"Exam Date:{exam_date}")
				p.drawString(100, y_position-80, f"Time: {start_time} to {end_time}")
				p.drawString(100, y_position-100, f"-" * 50)
				y_position -= 160
			p.showPage()
			p.save()
			buffer.seek(0)
			response = HttpResponse(content_type = 'application/pdf')
			response['Content-Disposition'] = 'attachment; filename="all_student_admit.pdf"'
			response['Conent-Length'] = len(buffer.getvalue())
			return response

	else:
		#Normal user
		if request.method == "POST":
			name = request.POST['name']
			father_name = request.POST['father_name']
			phone = request.POST['phone_number']
			student = Student.objects.filter(name=name, father_name=father_name, mobile_no=phone).first()
			examdetail = ExamDetails.objects.get(pk=1)
			buffer = BytesIO()
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="admit_card.pdf"'
			p = canvas.Canvas(buffer)
			p.drawString(100, 800, f"Name:{name}")
			p.drawString(100, 780, f"Roll No:{student.roll_number}")
			p.drawString(100, 740, f"Venue: {examdetail.venue}")
			p.drawString(100, 720, f"Exam Date:{examdetail.exam_date}")
			p.drawString(100, 700, f"Time: {examdetail.start_time} to {examdetail.end_time}")
			p.showPage()
			p.save()
			response.write(buffer.getvalue())
			return response
	return render(request, "student/generate_admit_card.html")
def enter_marks(request):
	if request.method == "POST":
		roll_no = request.POST.get("roll_number")
		marks = request.POST.get("marks")

		try:
			student = get_object_or_404(Student, roll_number=roll_no)
			if Marks.objects.filter(student=student).exists():
				messages.error(request, "Marks for this student already exist.")
			else:
				Marks.objects.create(student=student, marks=marks)
				messages.success(request, "Marks added successfully!")
		except Student.DoesNotExist:
			messages.error(request, "Student with this Roll Number does not exist.")
		return redirect("student:add_marks")
	return render(request ,"student/add_marks.html")

def get_marks_by_school(request):
	schools = School.objects.all()
	student_with_marks = None

	if request.method == "POST":
		school_name = request.POST.get("school_name")
		student_with_marks = Marks.objects.filter(student__school__name = school_name)
	return render(request, "student/marks_by_school.html", {"schools":schools, "student_with_marks":student_with_marks})

def all_results(request):
	student_with_marks = Marks.objects.all().order_by('-marks') # Sort by marks in descending order
	return render(request, "student/all_results.html", {"students_with_marks" : student_with_marks})
def download_results_pdf(request):
	student_with_marks = Marks.objects.all().order_by('-marks')

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="student_results.pdf"'

	p = canvas.Canvas(response)
	p.setFont("Helvetica", 12)

	y_position = 800

	p.drawString(200, y_position, "Student Results")
	y_position-=30

	for entry in student_with_marks:
		p.drawString(100, y_position, f"{entry.student.name} (Roll No: {entry.student.roll_number}) - Marks: {entry.marks}")
		y_position -= 20
	p.showPage()
	p.save()

	return response

