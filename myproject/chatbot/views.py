from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import random


@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").lower().strip()
    except:
        return JsonResponse({"reply": "Please type your question again."})

    # ---------------- CLEAN TEXT ----------------
    user_message = re.sub(r'[^\w\s]', '', user_message)

    # ---------------- FLEXIBLE MATCH ----------------
    def match_keywords(message, keywords):
        return any(word in message for word in keywords)

    # ---------------- INTENTS ----------------
    intents = [
        {
            "tag": "greeting",
            "keywords": ["hi", "hello", "hey", "good morning", "good evening"],
            "responses": [
                "Hello. Welcome to EduManage. How can I help you today?",
                "Hello. Are you looking for courses, fees, or admission details?"
            ]
        },

        {
            "tag": "courses",
            "keywords": ["course", "courses", "learn", "study"],
            "responses": [
                "We offer MS Excel and Graphic Design courses. Which one interests you?",
                "Our main courses are Excel and Graphic Design. I can guide you based on your interest."
            ]
        },

        {
            "tag": "best_course",
            "keywords": ["best course", "which course", "recommend", "suggest"],
            "responses": [
                "If you are a beginner, Excel is a good choice. If you are creative, you can choose Graphic Design.",
                "It depends on your interest. Excel is useful for office work, and Design is good for creative careers."
            ]
        },

        {
            "tag": "fees",
            "keywords": ["fees", "fee", "price", "cost", "charges"],
            "responses": [
                "Fees depend on the course. We also offer flexible installment options.",
                "Our fees are affordable. Which course are you interested in?"
            ]
        },

        {
            "tag": "duration",
            "keywords": ["duration", "how long", "months", "time"],
            "responses": [
                "Courses usually last between 1 to 6 months depending on your level.",
                "Duration depends on the course, typically between 1 to 6 months."
            ]
        },

        {
            "tag": "timing",
            "keywords": ["timing", "batch", "schedule", "time"],
            "responses": [
                "We have flexible batches: morning, afternoon, and evening.",
                "You can choose timing according to your convenience."
            ]
        },

        {
            "tag": "placement",
            "keywords": ["job", "placement", "career", "internship"],
            "responses": [
                "We help you become job-ready with placement support.",
                "We guide you with resume building and interview preparation."
            ]
        },

        {
            "tag": "demo",
            "keywords": ["demo", "trial", "sample class"],
            "responses": [
                "You can attend a free demo class before joining.",
                "We offer demo sessions so you can experience our teaching."
            ]
        },

        {
            "tag": "admission",
            "keywords": ["admission", "join", "enroll", "registration"],
            "responses": [
                "Admissions are open. You can visit our institute to enroll.",
                "You can join anytime. Visit us for quick registration."
            ]
        },

        {
            "tag": "contact",
            "keywords": ["contact", "phone", "address", "location"],
            "responses": [
                "You can visit our institute or contact us for more details.",
                "Our team is available to guide you. Feel free to contact or visit anytime."
            ]
        }
    ]

    # ---------------- MATCH MULTIPLE INTENTS ----------------
    matched_intents = []

    for intent in intents:
        if match_keywords(user_message, intent["keywords"]):
            matched_intents.append(intent)

    # ---------------- BUILD RESPONSE ----------------
    if matched_intents:
        replies = []

        for intent in matched_intents:
            replies.append(random.choice(intent["responses"]))

        final_reply = "\n\n".join(replies)

        # Suggestions
        suggestions = (
            "\n\nYou can also ask:\n"
            "- Fees\n"
            "- Course details\n"
            "- Duration\n"
            "- Placement"
        )

        final_reply += suggestions

        # CTA
        final_reply += "\n\nYou can visit our institute to get started."

        return JsonResponse({"reply": final_reply})

    # ---------------- FALLBACK ----------------
    fallback_responses = [
    "I can help you with courses, fees, admission, and timings. You can also contact us at 9867914107 or 9167683259, or email us at info@iceinstitute.com.",
    
    "Try asking about courses, fees, or placement. For direct assistance, call 9867914107 or 9167683259, or email info@iceinstitute.com.",
    
    "I am here to guide you. Ask anything about our institute. You can also reach us at 9867914107 / 9167683259 or info@iceinstitute.com."
]

    return JsonResponse({"reply": random.choice(fallback_responses)})