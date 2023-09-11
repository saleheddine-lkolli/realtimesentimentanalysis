import requests
import time

# Scrapyd base URL
scrapyd_url = 'http://localhost:6800'

# Define the job configurations
jobs = [
    {
      "job_id": "job01",
      "spider_name": "twitter_spider",
      "interval": 120  # Interval in seconds (e.g., 1 hour)
    },
    {
      "job_id": "job02",
      "spider_name": "twitter_spider",
      "interval": 120  # Interval in seconds (e.g., 1 hour)
    },
    {
      "job_id": "job03",
      "spider_name": "twitter_spider",
      "interval": 120  # Interval in seconds (e.g., 1 hour)
    },
]

# Schedule the jobs with delays
while True :
    for job in jobs:
        # Schedule the job
        response = requests.post(
            f'{scrapyd_url}/schedule.json',
            data={
            'project': 'twitterAPI',  # Adjust to your project name
            'spider': job['spider_name'],
            }
        )

        if response.status_code == 200:
            print(f"Scheduled job '{job['job_id']}' successfully.")
        else:
            print(f"Failed to schedule job '{job['job_id']}': {response.status_code} - {response.text}")

        # Sleep for 1 minute before scheduling the next job
        time.sleep(60)
        
    time.sleep(60)