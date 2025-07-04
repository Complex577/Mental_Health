from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
import langdetect
from dotenv import load_dotenv
from .models import SelfAssessment
from .models import FeatureModelAssignment


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


@api_view(["POST"])
def phq9_assessment(request):
    try:
        scores = request.data.get("scores", [])
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")
        age_group = request.data.get("age_group")
        sex = request.data.get("sex")

        if not scores or not isinstance(scores, list) or len(scores) != 9:
            return Response({"error": "Invalid or incomplete PHQ-9 scores."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)

        record = SelfAssessment.objects.create(
            user_type=user_type,
            age_group=age_group,
            sex=sex,
            score=total_score,
        )

        system_prompt = (
            f"You are Akili, a kind and supportive mental wellbeing assistant from PAWHA NGO. "
            f"A {user_type} has completed a screening for *msongo wa mawazo* (depression), and their total score is {total_score}/27. "
            f"The user is in the {age_group} age range and speaks {lang}. "
            f"Based on their score, provide a very short response (2–3 lines) that starts with something like: "
            f'**"Based on your score..."** and describe their emotional wellbeing briefly. '
            f"Do not say they *have* a condition — say they *might* be struggling or *seem* to be doing well. "
            f"Use bold, italic, quotes, or markdown if helpful. "
            f"Always end with a simple and polite suggestion of what they could do next. "
            f"Do not offer medical advice."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"PHQ-9 score: {total_score}. Respond in {lang}."}
        ]

        # 🔁 Dynamic model client
        client, model_name, temperature = get_model_client_for_feature("phq9")

        chat_response = client.chat.completions.create(
            model=model_name,
            messages=messages,
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
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")  # 'self' or 'student'
        age_group = request.data.get("age_group")  # e.g., '10-15'
        sex = request.data.get("sex")              # 'male', 'female', 'other'

        if not scores or not isinstance(scores, list) or len(scores) != 7:
            return Response({"error": "Invalid or incomplete GAD-7 scores."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)

        # Save assessment with incomplete data (contact fields null for now)
        record = SelfAssessment.objects.create(
            user_type=user_type,
            age_group=age_group,
            sex=sex,
            score=total_score,
        )

        system_prompt = (
            f"You are Akili, a kind and supportive mental wellbeing assistant from PAWHA NGO. "
            f"A {user_type} has completed a screening for *wasiwasi* (anxiety), and their total score is {total_score}/21. "
            f"The user is in the {age_group} age range and speaks {lang}. "
            f"Based on their score, provide a very short response (2–3 lines) that starts with something like: "
            f'**"Based on your score..."** and describe their emotional wellbeing briefly. '
            f"Do not say they *have* a condition — say they *might* be struggling or *seem* to be doing well. "
            f"You may use bold, italic, quotes, or markdown if helpful. "
            f"Always end with a simple and polite suggestion of what they could do next. "
            f"Do not offer medical advice. You are only a friendly assistant."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"GAD-7 score: {total_score}. Respond in {lang}."}
        ]

         # 🔁 Dynamic model client
        client, model_name, temperature = get_model_client_for_feature("gad7")

        chat_response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            stream=False
        )

        result = chat_response.choices[0].message.content.strip()

        # Determine if redirection is needed
        redirect_link = None
        if total_score >= 19:  # High risk score threshold
            redirect_link = f"/followup/{record.id}"

        return Response({
            "score": total_score,
            "response": result,
            "redirect_link": redirect_link
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
