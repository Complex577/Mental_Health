from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
import json

@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({'csrfToken': get_token(request)})


def check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'email': request.user.email,
                'name': request.user.get_full_name()
            }
        })
    return JsonResponse({'authenticated': False})@require_POST

def login_view(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data.get('email'), password=data.get('password'))

    if user is not None:
        login(request, user)

        # Check remember me flag from request
        remember = data.get('remember', False)

        if remember:
            # Set session expiry to 30 days (in seconds)
            request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            # Session will expire when the browser is closed
            request.session.set_expiry(0)

        return JsonResponse({
            'user': {
                'email': user.email,
                'name': user.get_full_name()
            }
        })

    return JsonResponse({'error': 'Invalid credentials'}, status=400)


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})


@login_required
def user_view(request):
    user = request.user
    return JsonResponse({'email': user.email, 'name': user.get_full_name()})


@require_POST
@login_required
def change_password(request):
    data = json.loads(request.body)
    user = request.user
    if not user.check_password(data.get("current_password")):
        return JsonResponse({"error": "Current password is incorrect."}, status=400)

    user.set_password(data.get("new_password"))
    user.save()
    return JsonResponse({"success": True})
