import requests
from django.conf import settings

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_brevo_email(
    to_email: str,
    subject: str,
    html_content: str,
):
    headers = {
        "accept": "application/json",
    
        "content-type": "application/json",
        "api-key": settings.BREVO_API_KEY,
    }

    payload = {
        "sender": {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL,
        },
        "to": [
            {"email": to_email}
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    response = requests.post(
        BREVO_API_URL,
        json=payload,
        headers=headers,
        timeout=10,
    )

    if response.status_code not in (200, 201):
        raise Exception(
            f"Brevo email failed: {response.status_code} | {response.text}"
        )

    return response.json()



