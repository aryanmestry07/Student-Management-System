from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Student, Result, Certificate


# ----------------------------
# STUDENT ADMIN
# ----------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'enrollment_date',
        'total_fees',
        'paid_amount',
        'pending_fees_display',
        'fees_status_display'
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'phone'
    )

    list_filter = ('enrollment_date', 'courses')  # ✅ removed fees_status

    filter_horizontal = ('courses',)

    # ✅ Show Pending Fees
    def pending_fees_display(self, obj):
        return obj.pending_fees

    pending_fees_display.short_description = "Pending Fees"

    # ✅ Show Status with color
    def fees_status_display(self, obj):
        if obj.fees_status == "Paid":
            return format_html('<span style="color:green;font-weight:bold;">Paid</span>')
        elif obj.fees_status == "Pending":
            return format_html('<span style="color:red;font-weight:bold;">Pending</span>')
        else:
            return format_html('<span style="color:orange;font-weight:bold;">Partial</span>')

    fees_status_display.short_description = "Status"


# ----------------------------
# RESULT ADMIN (MAIN CONTROL PANEL)
# ----------------------------
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks', 'status', 'certificate_button')
    list_filter = ('status', 'course')
    search_fields = ('student__user__username', 'course__name')
    ordering = ('-created_at',)

    def certificate_button(self, obj):
        if obj.status == "pass":
            url = reverse('student:generate_certificate', args=[obj.student.id, obj.course.id])
            return format_html(
                '<a class="button" style="background-color:green;color:white;padding:5px 10px;border-radius:5px;" href="{}" target="_blank">Generate / Download</a>',
                url
            )
        return format_html('<span style="color:red;">Not Eligible</span>')

    certificate_button.short_description = "Certificate"


# ----------------------------
# CERTIFICATE ADMIN (NEW 🔥)
# ----------------------------
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'certificate_id',
        'generated',
        'generated_at',
        'view_certificate'
    )

    search_fields = (
        'student__user__username',
        'course__name',
        'certificate_id'
    )

    list_filter = ('generated', 'course')

    ordering = ('-generated_at',)

    # 🔗 Open certificate PDF
    def view_certificate(self, obj):
        if obj.certificate_file:
            return format_html(
                '<a href="{}" target="_blank">Open</a>',
                obj.certificate_file.url
            )
        return "Not Generated"

    view_certificate.short_description = "Certificate File"