
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import get_template

def generate_invoice_pdf(order):
    # Render the HTML template to a string
    html_content = render_to_string('payment_pdf.html', {'order': order})

    # Create a BytesIO buffer to receive PDF data
    buffer = BytesIO()

    # Generate the PDF from the HTML content
    try:
        pisa_status = pisa.CreatePDF(html_content, dest=buffer)
        if pisa_status.err:
            raise Exception(f"PDF generation error: {pisa_status.err}")
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")

    # Go to the beginning of the buffer
    buffer.seek(0)

    return buffer



def send_invoice_email(recipient_email, pdf_content, order_id):
    # Print the email address (for debugging purposes)
    print(f"Sending email from: {settings.DEFAULT_FROM_EMAIL}")
    recipient_email=['chrisjohnjoy@gmail.com']
    # Create an EmailMessage object
    email = EmailMessage(
        subject=f'Invoice for Order #{order_id} from online medical store',
        body='Thank you for your order! Find the attached invoice.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_email,
    )

    # Attach the PDF content to the email
    email.attach(filename=f"Invoice_Order_{order_id}.pdf", content=pdf_content.getvalue(), mimetype='application/pdf')

    # Print the email password (for debugging purposes)
    print(f"Email password: {settings.EMAIL_HOST_PASSWORD}")

    # Send the email
    email.send()
