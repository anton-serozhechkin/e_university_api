import uvicorn

from settings import Settings

# Debugging
reload = False
reload_engine = "auto"
spew = False
check_config = False
print_config = False


# Server socket
HOST = f"{Settings.HOST}:{Settings.PORT}"
POST = "5432"
backlog = 2048


# Worker processes
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 100
max_requests_jitter = 4
timeout = 30
keepalive = 2


# Server mechanics
daemon = False
raw_env = []
pidfile = None
user = None
group = None
umask = 0
tmp_upload_dir = None


# Logging
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = "-"
loglevel = "info"
capture_output = False


# Process Naming
proc_name = None
default_proc_name = "gunicorn"


# Server Hooks
def on_starting(server):
    pass


def when_ready(server):
    pass


def pre_fork(server, worker):
    pass


def post_fork(server, worker):
    pass


def worker_int(worker):
    pass


def worker_abort(worker):
    pass


def pre_exec(server):
    pass
