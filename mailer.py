import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_alert_email(name, url, status, incident_start="", incident_end=""):

    message = Mail(
        from_email=os.getenv('SENDGRID_FROM_EMAIL'),
        to_emails=os.getenv('SENDGRID_TO_EMAIL')
    )

    message.dynamic_template_data = {
        'name': name,
        'url': url,
        'status': status,
        'incident_start': incident_start,
        'incident_end': incident_end
    }

    message.template_id = os.getenv('SENDGRID_DOWN_TEMPLATE_ID') if status == 'down' else os.getenv('SENDGRID_UP_TEMPLATE_ID')

    try:
        sendgrid_client = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print('{} alert for {} successfully sent...'.format(status, name))
    except Exception as e:
        print(e)
