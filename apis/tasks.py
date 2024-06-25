import logging

from celery import shared_task
from celery.utils.log import get_task_logger
import functools


logger = get_task_logger(__name__)


@functools.cache
def get_factor():
    logging.info('getting factor')
    return 5


@shared_task(queue='serial')
#@shared_task()
def prove_singleton(x):
    logging.info("running prove_singleton")
    f = get_factor()
    return f * x
