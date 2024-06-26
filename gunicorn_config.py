import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '1'))

threads = int(os.environ.get('GUNICORN_THREADS', '2'))

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

#bind = os.environ.get('GUNICORN_BIND', 'localhost:5000')



forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }