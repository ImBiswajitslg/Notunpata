import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = datetime.datetime.now().timestamp()

            if last_activity and now - last_activity > settings.SESSION_COOKIE_AGE:
                logout(request)
                return redirect('student:login')  # Redirect to login page after logout

            request.session['last_activity'] = now  # Update last activity time

        return self.get_response(request)
