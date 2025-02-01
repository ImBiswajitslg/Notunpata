from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
	path('register/', views.register_view, name="register"),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('admin_panel/', views.admin_panel, name="admin_panel"),
	path('add_marks/', views.enter_marks, name="add_marks"),
	path('list/', views.student_list, name='student_list'),
	path('add_student/', views.add_student, name="add_student"),
	path('student/', views.student, name="student"),
	path('generate_admit_card/', views.generate_admit_card, name="generate_admit_card"),
	path("marks-by-school/", views.get_marks_by_school, name="marks_by_school"),
	path('all-results/', views.all_results, name="all_results"),
	path('download-results/', views.download_results_pdf, name="download_results_pdf"),
]