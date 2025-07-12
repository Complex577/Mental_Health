import random
from datetime import timedelta
from django.utils import timezone
from self_evaluation.models import SelfAssessment  # adjust app name if needed

def run():
    user_types = ['self', 'student']
    sexes = ['male', 'female']
    phq_gad_age_groups = ['12-15', '16-20', '21-25', '26-30', '31-40', '40+']
    sdq_age_groups = ['4-7', '8-12', '13-17']

    assessments = []

    for _ in range(200):
        assessment_type = random.choice(['phq9', 'gad7', 'sdq'])
        user_type = random.choice(user_types)
        sex = random.choice(sexes)

        if assessment_type == 'sdq':
            age_group = random.choice(sdq_age_groups)
            score = random.randint(0, 40)
        else:
            age_group = random.choice(phq_gad_age_groups)
            score = random.randint(0, 27)

        assessment = SelfAssessment(
            user_type=user_type,
            assessment_type=assessment_type,
            age_group=age_group,
            sex=sex,
            score=score,
            contact_info=None,
            location=random.choice(['Dar es Salaam', 'Dodoma', 'Arusha', 'Mbeya', 'Mwanza']),
            description=random.choice(['', 'Reported fatigue and low mood.', 'Follow-up recommended.']),
            created_at=timezone.now() - timedelta(days=random.randint(0, 60))
        )
        assessments.append(assessment)

    SelfAssessment.objects.bulk_create(assessments)
    print(f"✅ Inserted {len(assessments)} synthetic assessments successfully.")


from self_evaluation.sythetic import run 
run()