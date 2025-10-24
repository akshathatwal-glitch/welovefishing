from flask import Flask, request
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Directory and file setup
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'clicks.csv')

# Ensure the logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# HTML for the fake 404 page
ERROR_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>404 Not Found</title>
    <style>
        body {
            background-color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            color: #222;
        }
        h1 {
            font-size: 80px;
            font-weight: bold;
            margin: 0;
        }
        p {
            font-size: 24px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>ERROR 404</h1>
    <p>website not available</p>
</body>
</html>
"""

@app.route('/')
def home():
    return ERROR_PAGE

@app.route('/phish-sim')
def log_click():
    email = request.args.get('teacher')  # Get email from URL param (?teacher=someone@gmail.com)
    if not email:
        return '❌ Missing "teacher" parameter in URL.', 400

    timestamp = datetime.now().isoformat()
    referrer = request.referrer or 'Direct'

    # Check if CSV exists before opening (so we can add header only once)
    new_file = not os.path.exists(LOG_FILE)

    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(['Email', 'Timestamp', 'Referrer'])
        writer.writerow([email, timestamp, referrer])

    # Return the styled fake error page
    return ERROR_PAGE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
