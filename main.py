import requests
from tinydb import TinyDB
from dotenv import load_dotenv
from datetime import datetime
from mailer import send_alert_email

db = TinyDB('db.json')
items = db.all()


def monitor_uptime():
    for item in items:

        name = item['name']
        url = item['url']
        status = item['status']
        incident_start = item['incident_start']
        incident_end = item['incident_end']

        res = requests.get(url)

        # initial down detection
        if res.status_code != 200 and status == 'up':
            item['status'] = 'down'
            status = item['status']
            item['incident_start'] = str(datetime.now())
            incident_start = item['incident_start']
            send_alert_email(name, url, status, incident_start)
            print('ALERT: {} is down'.format(name))

        # subsequent down detections
        # no need to continue sending emails
        elif res.status_code != 200 and status == 'down':
            print('[ALERT] {} is still down...'.format(name))

        # site is back up
        elif res.status_code == 200 and status == 'down':
            item['status'] = 'up'
            item['incident_end'] = str(datetime.now())
            status = item['status']
            incident_end = item['incident_end']
            send_alert_email(name, url, status, incident_start, incident_end)
            print("{} is back up:".format(name))

            # reset start/end values after email alert has been sent
            item['incident_start'] = ''
            item['incident_end'] = ''

        else:
            print('{} is up...'.format(name))

    db.write_back(items)


def main():
    load_dotenv()
    monitor_uptime()


if __name__ == '__main__':
    main()
