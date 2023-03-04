from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML
    
def export_pdf(request):
    
    # print("Request=======")
    # print(request)
    context = {}
    html = render_to_string("report-pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    # # font_config = FontConfiguration()
    HTML(string=html).write_pdf(response)

    return response