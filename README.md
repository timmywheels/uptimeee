# 🚨 Uptimeee | Get alerts when your sites go down

This project will periodically check the uptime of any URLs that are defined in `db.json` via the HTTP response code. If any none `200` HTTP response is returned, an alert email will be triggered.

### Getting started
Install dependencies by running `pip3 install -r requirements.txt`

Create a `db.json` file, paste the contents of `db.example.json` into it and update it with the details of the sites to be monitored.
Create a `.env` file, paste the contents of `.env.example` into it, and fill in the necessary values for the environment variables.


##### Environment Variables
- `UPTIME_POLL_INTERVAL`: The interval (in minutes) that you've specified for the cronjob to run the script
- `INCIDENT_ALERT_INTERVAL`: How often (in minutes) to send an email alert while a site is still down
- `SENDGRID_API_KEY`: Your Sendgrid API key
- `SENDGRID_DOWN_TEMPLATE_ID`: The Sendgrid template id for the template to be used for when a 'site down' alert is sent
- `SENDGRID_UP_TEMPLATE_ID`: The Sendgrid template id for the template to be used for when a 'site is back up' alert is sent
- `SENDGRID_FROM_EMAIL`: The email from which the Sendgrid emails will be sent
- `SENDGRID_TO_EMAIL`: The email to which the Sendgrid emails will be sent


Add sites to `db.json` - see below.

### Adding sites to monitor
This project utilizes a lightweight database called [`tinydb`](https://tinydb.readthedocs.io/en/latest/). The schema for each database record is as follows:
- `name`: The 'friendly name' of the site, project, or application to be monitored
- `url`: The URL that will be monitored for uptime
- `status`: The current status of the `url` - either `up` or `down`
- `incident_start`: The datetime at which the site went down
- `incident_end`: The datetime at which service was restored for the site
- `incident_length`: The length of time (in minutes) of the ongoing incident

Make sure to populate the `name` and `url` fields with the relevant info.  The `status` field should be set to `up`. You will also need to add the `incident_start` and `incident_end` fields, but make sure they're set to empty strings.

Example database:

```json
{
  "_default": {
    "1": {
      "name": "sendpoint.io",
      "url": "https://sendpoint.io",
      "status": "up",
      "incident_start": "",
      "incident_end": "",
      "incident_length": 0
    },
    "2": {
      "name": "Google",
      "url": "https://google.com",
      "status": "up",
      "incident_start": "",
      "incident_end": "",
      "incident_length": 0
    }
  }
}
```

### Setting up the cronjob
On the machine that will be executing the script, run the command `crontab -e` which will allow you to edit the crontab file. 

Define the cronjob like so (or however you see fit):

`* * * * * cd /path/to/project && /path/to/python3 /path/to/project/main.py > /dev/null 2>&1`

Example:
`* * * * * cd /root/dev/uptimeee && /usr/bin/python3 /root/dev/uptimeee/main.py > /dev/null 2>&1`

In this example, the cronjob - `* * * * *` - will execute `python3 main.py` every minute, and discard any output such as print statements as denoted by `> /dev/null 2>&1` 

Check out [crontab.guru](https://crontab.guru/#*_*_*_*_*) or [crontab-generator.org](https://crontab-generator.org/) for more info on defining cronjob intervals.

*NOTE:* Be sure that the `UPTIME_POLL_INTERVAL` environment variable in the `.env` file matches the cronjob interval


### Setting up the email alerts
This application utilizes the Sendgrid API to send email alerts when an outage has been detected. You will need to register for a [SendGrid](https://sendgrid.com) account and generate your API key to get started. 

You will then want to create a [transactional template](https://sendgrid.com/docs/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates/) (or two - perhaps one for the initial email alert, and another for when the site is back up) using the variables that are passed into the `message.dynamic_template_data` in `main.py`.
```python
    # example dynamic data in main.py
    message.dynamic_template_data = {
        'name': name,
        'url': url,
        'status': status
    }
```

Then you can reference those variables in the HTML of your email template using the [Handlebars.js Syntax](https://handlebarsjs.com/guide/#what-is-handlebars) like so:

```html
<!-- example sendgrid html email using dynamic data -->
<html>
    <h1>Uh oh! {{name}} appears to be {{status}}...</h1>
    <a href="{{url}}">See For Yourself</a>
</html>

```
