# Uptimeee.com

This project will periodically check the uptime of any URLs that are defined in `urls.txt` via the HTTP response code.

### Getting started
Install dependencies by running `pip install -r requirements.txt`

Add urls that you'd like to monitor to `urls.txt`

Create a `.env` file, paste the contents of `.env.example` into it, and fill in the necessary values

### Adding sites to monitor
This project utilizes a lightweight database called [`tinydb`](https://tinydb.readthedocs.io/en/latest/). The schema for each database record is as follows:
- `name`: The name of the 'friendly name' of the site, project, or application to be monitored
- `url`: The URL that will be monitored for uptime
- `status`: The current status of the `url` - either `up` or `down`
- `incident_start`: The datetime at which the site went down
- `incident_end`: The datetime at which service was restored for the site

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
      "incident_end": ""
    },
    "2": {
      "name": "CareerDevs",
      "url": "http://careerdevs.com",
      "status": "up",
      "incident_start": "",
      "incident_end": ""
    }
  }
}
```

 

### Setting up the cronjob
On the machine that will be executing the script, run the command `crontab -e` which will allow you to edit the crontab file. 

Define the cronjob like so (or however you see fit):

`* * * * * /path/to/python /path/to/main.py >/dev/null 2>&1`

In this example, the cronjob - `* * * * *` - will execute `python3 main.py` every minute, and discard any output such as print statements as denoted by `>/dev/null 2>&1` 

Check out [crontab.guru](https://crontab.guru/#*_*_*_*_*) or [crontab-generator.org](https://crontab-generator.org/) for more info on defining cronjob intervals.


### Setting up the email alerts
This application utilizes the Sendgrid API to send email alerts when an outage has been detected. You will need to register for a [SendGrid](https://sendgrid.com) account and generate your API key to get started. 

You will then want to create a transactional template using the variables that are passed into the `message.dynamic_template_data` in `main.py`. For instance, if you define a variable `url` within the dynamic template data, you will want to reference it in the HTML of your email template like so:

```python
    # example dynamic data in main.py
    message.dynamic_template_data = {
        'url': url,
    }
```


```html
<!-- example sendgrid html using dynamic data -->
<h1>Uh oh! {{url}} appears to be down...</h1>
```