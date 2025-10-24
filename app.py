from flask import Flask, request
import csv
from datetime import datetime

app = Flask(__name__)
log_file = 'clicks.csv'

@app.route('/phish-sim')
def log_click():
    email = request.args.get('teacher')  # Get Gmail from URL param
    timestamp = datetime.now().isoformat()  # Get current time
    referrer = request.referrer or 'Direct'

    # Save to CSV
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header if file is new
            writer.writerow(['Gmail', 'Timestamp', 'Referrer'])
        writer.writerow([email, timestamp, referrer])

    return 'Phishing Simulation Complete! You clicked the link.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)