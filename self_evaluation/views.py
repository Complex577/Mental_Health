from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
import langdetect
from dotenv import load_dotenv
from .models import SelfAssessment, FeatureModelAssignment

load_dotenv()

def get_model_client_for_feature(feature_key):
    assignment = FeatureModelAssignment.objects.select_related("model").filter(feature_key=feature_key).first()
    if not assignment or not assignment.model:
        raise Exception(f"No model assigned for feature '{feature_key}'")

    model = assignment.model
    if model.provider == "deepseek":
        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=model.base_url or "https://api.deepseek.com")
    elif model.provider == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise Exception(f"Unsupported provider: {model.provider}")

    return client, model.name, model.temperature

def generate_prompt(user_type, total_score, score_max, age_group, lang, question_score_pairs, is_child=False):
    prompt = (
        f"You are Akili, a kind and supportive mental wellbeing assistant from PAWHA NGO.\n"
        f"A {user_type} has completed a psychological screening and their total score is {total_score}/{score_max}.\n"
        f"They are in the {age_group} age group and communicate in {lang}.\n"
        f"Here are their individual question scores:\n"
    )

    for q, s in question_score_pairs:
        prompt += f"- {q} => {s}\n"

    prompt += ("\nPlease write a brief, kind response in markdown with the following sections:\n"
        "1. **Comment on the user's mental/emotional status.**\n"
        "2. **If score suggests concern, list possible causes.**\n"
        f"3. {'The user is a teacher/guardian filling the form for a child, suggest ways he/she can help the child.' if is_child else 'Suggest simple self-help or support actions.'}\n"
        "4. **End with hope-giving and encouraging words.**\n"
        "Not necessary to list the sections as they are exactly use but generatively or use lines and to seperate concerns.**\n"
        "You are replying to the user, use emojis.**\n"
        "Be breif.**\n"
        "Use the user's language. Do not give medical advice.")

    return prompt

@api_view(["POST"])
def phq9_assessment(request):
    try:
        scores = request.data.get("scores", [])
        responses = request.data.get("responses", [])
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")
        age_group = request.data.get("age_group")
        sex = request.data.get("sex")

        questions = [r.get("question") for r in responses]

        if not scores or not questions or len(scores) != 9 or len(questions) != 9:
            return Response({"error": "Invalid or incomplete PHQ-9 input."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)

        record = SelfAssessment.objects.create(
            user_type=user_type,
            age_group=age_group,
            sex=sex,
            score=total_score
        )

        prompt = generate_prompt(user_type, total_score, 27, age_group, lang, zip(questions, scores))

        client, model_name, temperature = get_model_client_for_feature("phq9")
        chat_response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=False
        )

        result = chat_response.choices[0].message.content.strip()
        redirect_link = f"/followup/{record.id}" if total_score >= 19 else None

        return Response({
            "score": total_score,
            "response": result,
            "redirect_link": redirect_link
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def gad7_assessment(request):
    try:
        scores = request.data.get("scores", [])
        responses = request.data.get("responses", [])
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")
        age_group = request.data.get("age_group")
        sex = request.data.get("sex")

        questions = [r.get("question") for r in responses]

        if not scores or not questions or len(scores) != 7 or len(questions) != 7:
            return Response({"error": "Invalid or incomplete GAD-7 input."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)
        record = SelfAssessment.objects.create(user_type=user_type, age_group=age_group, sex=sex, score=total_score)

        prompt = generate_prompt(user_type, total_score, 21, age_group, lang, zip(questions, scores))

        client, model_name, temperature = get_model_client_for_feature("gad7")
        chat_response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=False
        )

        result = chat_response.choices[0].message.content.strip()
        redirect_link = f"/followup/{record.id}" if total_score >= 19 else None

        return Response({"score": total_score, "response": result, "redirect_link": redirect_link}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def child_assessment(request):
    try:
        scores = request.data.get("scores", [])
        responses = request.data.get("responses", [])
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")
        age_group = request.data.get("age_group")
        sex = request.data.get("sex")

        questions = [r.get("question") for r in responses]

        if not scores or not questions or len(scores) != len(questions):
            return Response({"error": "Invalid or incomplete SDQ input."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)
        record = SelfAssessment.objects.create(user_type=user_type, age_group=age_group, sex=sex, score=total_score)

        prompt = generate_prompt(user_type, total_score, 50, age_group, lang, zip(questions, scores), is_child=True)

        client, model_name, temperature = get_model_client_for_feature("sdq")
        chat_response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=False
        )

        result = chat_response.choices[0].message.content.strip()
        redirect_link = f"/followup/{record.id}" if total_score >= 19 else None

        return Response({"score": total_score, "response": result, "redirect_link": redirect_link}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def update_followup_details(request, pk):
    try:
        assessment = SelfAssessment.objects.get(pk=pk)

        contact_info = request.data.get("contact_info")
        location = request.data.get("location")
        description = request.data.get("description")

        if not contact_info or not location:
            return Response({"error": "Contact info and location are required."}, status=status.HTTP_400_BAD_REQUEST)

        assessment.contact_info = contact_info
        assessment.location = location
        assessment.description = description
        assessment.save()

        return Response({"message": "Details updated successfully."}, status=status.HTTP_200_OK)

    except SelfAssessment.DoesNotExist:
        return Response({"error": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
