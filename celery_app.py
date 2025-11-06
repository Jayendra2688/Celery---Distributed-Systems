import os
from celery import Celery

app = Celery(
    "flowpilot",
    broker='redis://127.0.0.1:6379/0',     # Redis broker
    backend='redis://127.0.0.1:6379/1'    # Redis result backend
)
import tasks