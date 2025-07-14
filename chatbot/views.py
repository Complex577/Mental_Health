# chatbot/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
import langdetect
from dotenv import load_dotenv
load_dotenv()


openai_key = os.getenv("OPENAI_API_KEY")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key= openai_key)
client_deepseek = OpenAI(api_key= deepseek_key,  base_url="https://api.deepseek.com")

# Define a helper to check if it's mental health-related (simple keyword filter for now)
MENTAL_HEALTH_KEYWORDS = [
    "stress", "depression", "anxiety", "lonely", "mental", "wellbeing", "panic",
    "trauma", "abuse", "grief", "therapy", "counseling", "self-harm", "burnout", "sad"
]

def is_mental_health_related(text):
    return any(keyword in text.lower() for keyword in MENTAL_HEALTH_KEYWORDS)

@api_view(["POST"])

def akili_chat(request):
    try:
        user_input = request.data.get("message", "")
        history = request.data.get("history", [])[-5:]

        if not user_input:
            return Response({"error": "No message provided."}, status=status.HTTP_400_BAD_REQUEST)

        #if not is_mental_health_related(user_input):
        #    return Response({"response": "Akili is here to support your mental health. Please ask about mental wellness, stress, anxiety, or emotional support."})

        # Detect user language
        lang = langdetect.detect(user_input)

        messages = [
            {
                "role": "system",
                "content": (
                    f"You are Akili, a supportive and empathetic AI created by PAWHA (Pan-Africa Women in Health Association), "
                    f"a non-profit NGO. You specialize strictly in mental health support. "
                    f"You do not answer questions unrelated to mental health. "
                    f"Respond only in the user's language. "
                    f"Format your answers using **bold**, *italic*, [links](https://...), and > quotes. "
                    f"Use markdown only. Do not mention any capabilities outside of mental health. "
                    f"If the user asks non-mental health questions, gently decline with a supportive tone."
                )
            }
        ]

        # Append the previous 5 user inputs
        messages += [{"role": "user", "content": m} for m in history]

        # Append the current user input
        messages.append({"role": "user", "content": user_input})

        chat_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )

        content = chat_response.choices[0].message.content
        return Response({"response": content})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(["POST"])

def akili_chat_deepseek(request):
    try:
        user_input = request.data.get("message", "")
        history = request.data.get("history", [])[-10:]

        if not user_input:
            return Response({"error": "No message provided."}, status=status.HTTP_400_BAD_REQUEST)

        #if not is_mental_health_related(user_input):
        #    return Response({"response": "Akili is here to support your mental health. Please ask about mental wellness, stress, anxiety, or emotional support."})

        # Detect user language
        lang = langdetect.detect(user_input)

        messages = [
            {
                "role": "system",
                "content": (
                    f"You are Akili, a supportive and empathetic AI created by PAWHA (Pan-Africa Women in Health Association), "
                    f"a non-profit NGO, Specializing in general global health solutions such as mental health support, HIV/AIDS and Climate change effects on health. But you specialize strictly in mental health support. "
                    f"You do not answer questions unrelated to mental health. "
                    f"Respond only in the user's language. "
                    f"Format your answers using **bold**, *italic*, [links](https://...), and > quotes. "
                    f"Use markdown only. Do not mention any capabilities outside of mental health. "
                    f"Address mental health as psychology and emotions, do not use mental or mental health words."
                    f"Give short and brief responses to greetings."
                    f"Your work is to provide assistance and solutions to the user."
                    f"The only links you can provide are Tanzanian mental health approved platforms as pawha.org as your organization's site with this phone number +255 773 815 955 and this email address support@pawha.org."
                    F"Provide the contacts and links only if the user wants them or only when you detect the user is in a critical condition."
                    f"If the user asks non-mental health questions, gently decline with a supportive tone."
                    
                )
            }
        ]

        # Append the previous 5 user inputs
        for m in history:
            if isinstance(m, dict) and "sender" in m and "text" in m:
                messages.append({
                    "role": "user" if m["sender"] == "user" else "assistant",
                    "content": m["text"]
                })

        # Append the current user input
        messages.append({"role": "user", "content": user_input})

        chat_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            # stream=False
        )

        content = chat_response.choices[0].message.content
        return Response({"response": content})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
