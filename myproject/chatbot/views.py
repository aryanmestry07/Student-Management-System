from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()
    except:
        return JsonResponse({"reply": "Please type your question again 😊"})

    intents = {
        # ---------------- BASIC ----------------
        "greeting": {
            "keywords": ["hi", "hello", "hey", "good morning", "good evening"],
            "reply": "Hello 👋 Welcome to our Computer Institute. How can I help you today?"
        },
        "about_institute": {
            "keywords": ["about", "institute", "who are you", "information"],
            "reply": "We are a professional computer training institute offering job-oriented courses in MS Excel and Graphic Design."
        },

        # ---------------- COURSES ----------------
        "courses": {
            "keywords": ["course", "courses", "program", "what do you teach"],
            "reply": "We offer MS Excel (Basic to Advanced) and Graphic Design courses using Photoshop, Illustrator, and CorelDraw."
        },
        "excel_course": {
            "keywords": ["excel", "ms excel", "spreadsheet"],
            "reply": "Our MS Excel course covers basics, formulas, functions, charts, data analysis, and real-world office work."
        },
        "design_course": {
            "keywords": ["graphic", "design", "photoshop", "illustrator", "coreldraw"],
            "reply": "Graphic Design course includes Photoshop, Illustrator, CorelDraw, logo design, posters, banners, and social media creatives."
        },

        # ---------------- FEES ----------------
        "fees": {
            "keywords": ["fees", "fee", "cost", "price", "charges"],
            "reply": "Course fees depend on the selected course and duration. Please visit the institute or contact us for exact fee details."
        },
        "payment": {
            "keywords": ["installment", "payment", "pay", "emi"],
            "reply": "Yes, fee payment in installments is available for selected courses."
        },

        # ---------------- DURATION ----------------
        "duration": {
            "keywords": ["duration", "how long", "months", "time"],
            "reply": "Courses range from 1 month to 6 months depending on the program and learning speed."
        },

        # ---------------- ADMISSION ----------------
        "admission": {
            "keywords": ["admission", "apply", "join", "enroll", "registration"],
            "reply": "Admissions are open throughout the year. You can directly visit the institute to enroll."
        },
        "documents": {
            "keywords": ["document", "documents", "required", "marksheet"],
            "reply": "You only need a basic ID proof and passport-size photographs for admission."
        },

        # ---------------- ELIGIBILITY ----------------
        "eligibility": {
            "keywords": ["eligibility", "qualification", "who can join"],
            "reply": "Anyone can join. No prior technical knowledge is required for basic courses."
        },
        "age": {
            "keywords": ["age", "minimum age", "school student"],
            "reply": "Students above 14 years can enroll. School and college students are welcome."
        },

        # ---------------- CLASS MODE ----------------
        "mode": {
            "keywords": ["online", "offline", "class mode"],
            "reply": "We offer both offline classroom training and online live classes."
        },
        "batch_timing": {
            "keywords": ["timing", "batch", "schedule", "class time"],
            "reply": "Flexible batch timings are available: morning, afternoon, and evening."
        },
        "weekend": {
            "keywords": ["weekend", "saturday", "sunday"],
            "reply": "Yes, weekend batches are available for working professionals and students."
        },

        # ---------------- DEMO ----------------
        "demo": {
            "keywords": ["demo", "trial", "sample class"],
            "reply": "Yes 😊 Demo classes are available before admission."
        },

        # ---------------- CERTIFICATE ----------------
        "certificate": {
            "keywords": ["certificate", "certification"],
            "reply": "You will receive a course completion certificate after successfully finishing the course."
        },

        # ---------------- PLACEMENT ----------------
        "placement": {
            "keywords": ["job", "placement", "career", "internship"],
            "reply": "We provide placement assistance, resume guidance, and interview preparation."
        },

        # ---------------- FACULTY ----------------
        "faculty": {
            "keywords": ["faculty", "teacher", "trainer", "experience"],
            "reply": "Our trainers are experienced professionals with industry and teaching expertise."
        },

        # ---------------- INFRASTRUCTURE ----------------
        "lab": {
            "keywords": ["lab", "computer lab", "infrastructure", "facility"],
            "reply": "We have well-equipped computer labs with high-speed internet and latest software."
        },
        "laptop": {
            "keywords": ["laptop", "computer", "own laptop"],
            "reply": "No need to bring a laptop. Systems are provided in the lab."
        },

        # ---------------- SOFTWARE ----------------
        "software": {
            "keywords": ["software", "tools", "photoshop license"],
            "reply": "All required software like MS Excel and design tools are provided during training."
        },

        # ---------------- ATTENDANCE ----------------
        "attendance": {
            "keywords": ["attendance", "absent", "miss class"],
            "reply": "If you miss a class, backup sessions or doubt-clearing support is provided."
        },

        # ---------------- WORKING DAYS ----------------
        "working_days": {
            "keywords": ["working days", "open", "office hours"],
            "reply": "We are open Monday to Saturday from 9 AM to 8 PM."
        },

        # ---------------- REFUND ----------------
        "refund": {
            "keywords": ["refund", "cancel", "money back"],
            "reply": "Refund policies depend on the course. Please confirm details at the admission desk."
        },

        # ---------------- PARENTS ----------------
        "parents": {
            "keywords": ["parent", "parents", "guardian"],
            "reply": "Parents are welcome to visit the institute and discuss course details anytime."
        },

        # ---------------- CONTACT ----------------
        "contact": {
            "keywords": ["contact", "phone", "call", "number", "email", "address"],
            "reply": "You can contact us directly by visiting the institute or calling our office number."
        },

        # ---------------- THANKS ----------------
        "thanks": {
            "keywords": ["thanks", "thank you", "thx"],
            "reply": "You're welcome 😊 Happy learning!"
        }
    }

    best_reply = None
    max_score = 0

    for intent in intents.values():
        score = sum(1 for word in intent["keywords"] if word in user_message)
        if score > max_score:
            max_score = score
            best_reply = intent["reply"]

    # VERY SOFT FALLBACK (NO ERROR FEEL)
    if max_score == 0:
        best_reply = (
            "I can help you with courses, fees, admissions, Excel, Graphic Design, "
            "certificates, batch timings, and placement assistance 😊"
        )

    return JsonResponse({"reply": best_reply})
