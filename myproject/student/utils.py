from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from django.conf import settings
from datetime import datetime
import os


def generate_certificate(student, course, certificate):
    file_name = f"certificate_{student.id}_{course.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, "certificates", file_name)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles['Title'],
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontSize=28,
        spaceAfter=20
    )

    center_style = ParagraphStyle(
        name="CenterStyle",
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=14,
        spaceAfter=10
    )

    name_style = ParagraphStyle(
        name="NameStyle",
        parent=styles['Heading2'],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=15
    )

    course_style = ParagraphStyle(
        name="CourseStyle",
        parent=styles['Heading3'],
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontSize=18,
        spaceAfter=20
    )

    content = []

    content.append(Spacer(1, 40))
    content.append(Paragraph("CERTIFICATE OF COMPLETION", title_style))

    content.append(Paragraph("This is to certify that", center_style))
    content.append(Paragraph(f"<b>{student.full_name}</b>", name_style))
    content.append(Paragraph("has successfully completed the course", center_style))
    content.append(Paragraph(f"<b>{course.name}</b>", course_style))

    content.append(Spacer(1, 30))
    content.append(Paragraph(f"Date: {datetime.now().strftime('%d %B %Y')}", center_style))

    # ✅ ADD CERTIFICATE ID HERE (CORRECT)
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Certificate ID: {certificate.certificate_id}", center_style))

    content.append(Spacer(1, 60))
    content.append(Paragraph("__________________________", center_style))
    content.append(Paragraph("Authorized Signature", center_style))

    content.append(Spacer(1, 20))
    content.append(Paragraph("EduManage Learning System", center_style))

    doc.build(content)

    return f"certificates/{file_name}"