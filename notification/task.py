from common_library import send_email
from config.celery import app


@app.task
def send_email_async_notification(title: str, html_body_content: str, payload: dict, to: list) -> None:
    send_email(
        title=title,
        html_body_content=html_body_content,
        payload=payload,
        to=to,
    )
