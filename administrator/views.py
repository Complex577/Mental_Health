from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count
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


@login_required
@require_http_methods(["GET"])
def sdq_stats(request):
    qs = SelfAssessment.objects.filter(assessment_type='sdq')

    total = qs.count()
    average_score = qs.aggregate(avg=Avg('score'))['avg'] or 0
    high_risk = qs.filter(score__gte=17).count()  # High risk threshold for SDQ
    last_updated = qs.order_by('-created_at').first().created_at if total else None

    # User type and sex breakdown
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

    # Age group breakdown (for children)
    age_groups = ['4-7', '8-12', '13-17']
    age_group_chart = [
        {'age_group': group, 'count': qs.filter(age_group=group).count()}
        for group in age_groups
    ]

    # Score ranges for SDQ (Total Difficulty Score: 0–40)
    score_ranges = {
        'Normal (0–13)': (0, 13),
        'Borderline (14–16)': (14, 16),
        'Abnormal (17–40)': (17, 40),
    }
    score_range_data = [
        {'label': label, 'count': qs.filter(score__gte=low, score__lte=high).count()}
        for label, (low, high) in score_ranges.items()
    ]

    # Recent submissions (last 10)
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

from django.core.paginator import Paginator


@login_required
@require_http_methods(["GET"])
def referral_stats_view(request):
    page = int(request.GET.get("page", 1))
    per_page = 10

    # Get base queryset
    base_qs = SelfAssessment.objects.filter(location__isnull=False)

    # Create breakdown BEFORE ordering
    assessment_breakdown = base_qs.values("assessment_type").annotate(count=Count("id"))
    breakdown = {item["assessment_type"]: item["count"] for item in assessment_breakdown}

    # Now order for pagination
    qs = base_qs.order_by("-score", "-created_at")
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page)

    data = list(page_obj.object_list.values(
        "id", "assessment_type", "score", "location",
        "contact_info", "description", "created_at"
    ))

    return JsonResponse({
        "results": data,
        "total": base_qs.count(),
        "total_pages": paginator.num_pages,
        "breakdown": breakdown,
    })


@login_required
@require_http_methods(["GET"])
def dashboard_view(request):
    # PHQ9 stats
    phq9_qs = SelfAssessment.objects.filter(assessment_type='phq9')
    phq9_total = phq9_qs.count()

    # Example PHQ9 score ranges and counts
    phq9_score_ranges = {
        'Minimal (0-4)': (0, 4),
        'Mild (5-9)': (5, 9),
        'Moderate (10-14)': (10, 14),
        'Moderately Severe (15-19)': (15, 19),
        'Severe (20-27)': (20, 27),
    }
    phq9_distribution = [
        {'label': label, 'count': phq9_qs.filter(score__gte=low, score__lte=high).count()}
        for label, (low, high) in phq9_score_ranges.items()
    ]
    phq9_chart = {
        'labels': [d['label'] for d in phq9_distribution],
        'datasets': [{
            'label': 'PHQ9 Scores',
            'backgroundColor': '#f87171',
            'data': [d['count'] for d in phq9_distribution]
        }]
    }

    # GAD7 stats
    gad7_qs = SelfAssessment.objects.filter(assessment_type='gad7')
    gad7_total = gad7_qs.count()
    gad7_score_ranges = {
        'Minimal (0-4)': (0, 4),
        'Mild (5-9)': (5, 9),
        'Moderate (10-14)': (10, 14),
        'Severe (15-21)': (15, 21),
    }
    gad7_distribution = [
        {'label': label, 'count': gad7_qs.filter(score__gte=low, score__lte=high).count()}
        for label, (low, high) in gad7_score_ranges.items()
    ]
    gad7_chart = {
        'labels': [d['label'] for d in gad7_distribution],
        'datasets': [{
            'label': 'GAD7 Scores',
            'backgroundColor': '#60a5fa',
            'data': [d['count'] for d in gad7_distribution]
        }]
    }

    # SDQ stats
    sdq_qs = SelfAssessment.objects.filter(assessment_type='sdq')
    sdq_total = sdq_qs.count()
    # For SDQ, let's bucket scores as Low, Medium, High
    sdq_score_ranges = {
        'Low (0-13)': (0, 13),
        'Medium (14-17)': (14, 17),
        'High (18-40)': (18, 40),
    }
    sdq_distribution = [
        {'label': label, 'count': sdq_qs.filter(score__gte=low, score__lte=high).count()}
        for label, (low, high) in sdq_score_ranges.items()
    ]
    sdq_chart = {
        'labels': [d['label'] for d in sdq_distribution],
        'datasets': [{
            'label': 'SDQ Scores',
            'backgroundColor': '#34d399',
            'data': [d['count'] for d in sdq_distribution]
        }]
    }

    # Referrals summary (records with location)
    referrals_qs = SelfAssessment.objects.filter(location__isnull=False)
    referrals_total = referrals_qs.count()
    referrals_breakdown_qs = referrals_qs.values('assessment_type').annotate(count=Count('id'))
    referrals_breakdown = {
        item['assessment_type']: item['count'] for item in referrals_breakdown_qs
    }
    referrals_chart = {
        'labels': list(referrals_breakdown.keys()),
        'datasets': [{
            'label': 'Referrals',
            'backgroundColor': '#fbbf24',
            'data': list(referrals_breakdown.values())
        }]
    }

    # Recent high risk (score >= 15) assessments (latest 10)
    recent_high_risk = SelfAssessment.objects.filter(score__gte=15).order_by('-created_at')[:10]
    recent_data = list(recent_high_risk.values('id', 'assessment_type', 'score', 'location', 'created_at'))

    return JsonResponse({
        'phq9': {
            'total': phq9_total,
            'score_distribution': phq9_chart,
        },
        'gad7': {
            'total': gad7_total,
            'score_distribution': gad7_chart,
        },
        'sdq': {
            'total': sdq_total,
            'score_distribution': sdq_chart,
        },
        'referrals': {
            'total': referrals_total,
            'breakdown': referrals_chart,
        },
        'recent_high_risk': recent_data,
    })



from rest_framework.response import Response
from education.models import ContentNode
from .serializers import ContentNodeSerializer

@login_required
@require_http_methods(["GET"])
def list_root_nodes(request):
    node_type = request.GET.get("type")
    if not node_type:
        return JsonResponse({"error": "Missing 'type' parameter."}, status=400)

    nodes = ContentNode.objects.filter(parent__isnull=True, node_type=node_type).order_by('created_at')
    serializer = ContentNodeSerializer(nodes, many=True)
    return JsonResponse(serializer.data, safe=False)


@login_required
@require_http_methods(["POST"])
def create_node(request):
    data = json.loads(request.body.decode('utf-8'))

    serializer = ContentNodeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@login_required
@require_http_methods(["PUT"])
def update_node(request, pk):
    try:
        node = ContentNode.objects.get(pk=pk)
    except ContentNode.DoesNotExist:
        return JsonResponse({"error": "Not found."}, status=404)

    data = json.loads(request.body.decode('utf-8'))
    data['updated_at'] = now()

    serializer = ContentNodeSerializer(node, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


@login_required
@require_http_methods(["DELETE"])
def delete_node(request, pk):
    try:
        node = ContentNode.objects.get(pk=pk)
    except ContentNode.DoesNotExist:
        return JsonResponse({"error": "Not found."}, status=404)

    node.delete()
    return JsonResponse({"message": "Deleted."}, status=204)

