from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
import json

from django.utils.timezone import now
from django.db.models import Avg
from self_evaluation.models import SelfAssessment


# ---------------- CSRF + Auth Management ---------------- #

@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({"message": "CSRF cookie set"})


def check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'email': request.user.email,
                'name': request.user.get_full_name()
            }
        })
    return JsonResponse({'authenticated': False})


@require_POST
def login_view(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data.get('email'), password=data.get('password'))

    if user is not None:
        login(request, user)

        # Session expiration logic
        remember = data.get('remember', False)
        request.session.set_expiry(60 * 60 * 24 * 30 if remember else 0)

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


# ---------------- PHQ-9 Dashboard Stats ---------------- #

@login_required
@require_http_methods(["GET"])
def phq9_stats(request):
    qs = SelfAssessment.objects.filter(assessment_type='phq9')

    total = qs.count()
    average_score = qs.aggregate(avg=Avg('score'))['avg'] or 0
    high_risk = qs.filter(score__gte=15).count()
    last_updated = qs.order_by('-created_at').first().created_at if total else None

    # User type & sex chart
    user_types = ['self', 'student']
    sexes = ['male', 'female']
    user_sex_chart = [
        {
            'user_type': ut,
            'sex': sex,
            'count': qs.filter(user_type=ut, sex=sex).count()
        }
        for ut in user_types
        for sex in sexes
    ]

    # Age group distribution
    age_groups = ['12-15', '16-20', '21-25', '26-30', '31-40', '40+']
    age_group_chart = [
        {'age_group': group, 'count': qs.filter(age_group=group).count()}
        for group in age_groups
    ]

    # Score range breakdown
    score_ranges = {
        'Minimal (0-4)': (0, 4),
        'Mild (5-9)': (5, 9),
        'Moderate (10-14)': (10, 14),
        'Moderately Severe (15-19)': (15, 19),
        'Severe (20-27)': (20, 27),
    }
    score_range_data = [
        {'label': label, 'count': qs.filter(score__gte=low, score__lte=high).count()}
        for label, (low, high) in score_ranges.items()
    ]

    # Recent assessments table
    recent = qs.order_by('-created_at')[:10].values(
        'user_type', 'sex', 'age_group', 'score', 'created_at'
    )

    return JsonResponse({
        'total': total,
        'average_score': round(average_score, 2),
        'high_risk': high_risk,
        'last_updated': last_updated,
        'user_sex_chart': user_sex_chart,
        'age_group_chart': age_group_chart,
        'score_ranges': score_range_data,
        'recent': list(recent),
    })

@login_required
@require_http_methods(["GET"])
def gad7_stats(request):
    qs = SelfAssessment.objects.filter(assessment_type='gad7')

    total = qs.count()
    average_score = qs.aggregate(avg=Avg('score'))['avg'] or 0
    high_risk = qs.filter(score__gte=15).count()  # GAD-7 high risk threshold often ≥15
    last_updated = qs.order_by('-created_at').first().created_at if total else None

    # User type & sex chart
    user_types = ['self', 'student']
    sexes = ['male', 'female']
    user_sex_chart = [
        {
            'user_type': ut,
            'sex': sex,
            'count': qs.filter(user_type=ut, sex=sex).count()
        }
        for ut in user_types
        for sex in sexes
    ]

    # Age group distribution (GAD-7 uses adult brackets)
    age_groups = ['12-15', '16-20', '21-25', '26-30', '31-40', '40+']
    age_group_chart = [
        {'age_group': group, 'count': qs.filter(age_group=group).count()}
        for group in age_groups
    ]

    # Score range breakdown (specific for GAD-7: max = 21)
    score_ranges = {
        'Minimal (0-4)': (0, 4),
        'Mild (5-9)': (5, 9),
        'Moderate (10-14)': (10, 14),
        'Severe (15-21)': (15, 21),
    }
    score_range_data = [
        {'label': label, 'count': qs.filter(score__gte=low, score__lte=high).count()}
        for label, (low, high) in score_ranges.items()
    ]

    # Recent assessments
    recent = qs.order_by('-created_at')[:10].values(
        'user_type', 'sex', 'age_group', 'score', 'created_at'
    )

    return JsonResponse({
        'total': total,
        'average_score': round(average_score, 2),
        'high_risk': high_risk,
        'last_updated': last_updated,
        'user_sex_chart': user_sex_chart,
        'age_group_chart': age_group_chart,
        'score_ranges': score_range_data,
        'recent': list(recent),
    })