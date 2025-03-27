# gunicorn_config.py
import multiprocessing

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class (sync is default, gevent can be used for async)
worker_class = 'sync'

# Bind to all network interfaces
bind = '0.0.0.0:8000'

# Timeout settings
timeout = 120

# Keepalive
keepalive = 5

# Maximum number of simultaneous clients
worker_connections = 1000

# Logging
accesslog = '-'  # stdout
errorlog = '-'   # stderr
loglevel = 'info'

# Preload the application
preload_app = True

# Additional worker-related settings
max_requests = 1000  # Restart workers after 1000 requests
max_requests_jitter = 50  # Add randomness to worker restarts