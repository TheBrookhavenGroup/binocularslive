import logging

from celery import shared_task
from celery.utils.log import get_task_logger
import functools


logger = get_task_logger(__name__)


@functools.cache
def get_factor():
    logging.debug('getting factor')
    return 5


@shared_task(queue='serial')
def prove_singleton(x):
    logging.debug("running prove_singleton")
    f = get_factor()
    return f * x
