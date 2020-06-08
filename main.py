import os
import requests
import logging
from tinydb import TinyDB
from dotenv import load_dotenv
from datetime import datetime
from mailer import send_alert_email

db = TinyDB('db.json')
items = db.all()

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def monitor_uptime():

    uptime_poll_interval = os.getenv('UPTIME_POLL_INTERVAL')
    incident_alert_interval = int(os.getenv('INCIDENT_ALERT_INTERVAL'))

    for item in items:

        name = item['name']
        url = item['url']
        status = item['status']
        incident_start = item['incident_start']
        incident_end = item['incident_end']
        incident_length = item['incident_length']

        res = requests.get(url)

        # initial down detection
        if res.status_code != 200 and status == 'up':
            item['status'] = 'down'
            status = item['status']
            item['incident_start'] = str(datetime.now())
            incident_start = item['incident_start']
            send_alert_email(name, url, status, incident_start)
            logger.error('ALERT: {} is down'.format(name))

        # subsequent down detections
        # no need to continue sending emails
        # unless incident has reached specified alert interval
        elif res.status_code != 200 and status == 'down':
            if incident_length > 0 and incident_length % incident_alert_interval == 0:
                send_alert_email(name, url, status, incident_start)
            logger.info('[ALERT] {} is still down...'.format(name))
            item['incident_length'] = incident_length + int(uptime_poll_interval)

        # site is back up
        elif res.status_code == 200 and status == 'down':
            item['status'] = 'up'
            item['incident_end'] = str(datetime.now())
            status = item['status']
            incident_end = item['incident_end']
            send_alert_email(name, url, status, incident_start, incident_end)
            logger.info("{} is back up:".format(name))

            # reset values after email alert has been sent
            item['incident_start'] = ''
            item['incident_end'] = ''
            item['incident_length'] = 0

        else:
            logger.info('{} is up...'.format(name))

    db.write_back(items)


def main():
    load_dotenv()
    monitor_uptime()


if __name__ == '__main__':
    main()
